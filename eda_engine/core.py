# eda_engine/core.py
"""
EDA: an on-demand exploratory-data-analysis facade.

Use it the way you use pandas/matplotlib — create one object, then call only
the pieces you want, when you want them:

    from eda_engine import EDA

    eda = EDA(df)

    eda.schema              # cached schema (computed once)
    eda.overview()          # quick shape / type summary  -> DataFrame
    eda.missing()           # missing-value report        -> DataFrame
    eda.duplicates()        # duplicate / key report       -> dict
    eda.describe_numeric()  # numeric stats               -> DataFrame
    eda.describe_categorical()
    eda.describe_boolean()
    eda.value_counts("Sex") # pandas-style convenience

    eda.plot_distribution("Age")    # returns a Matplotlib Figure (renders inline)
    eda.plot_counts("Pclass")
    eda.plot_correlation()
    eda.plot_missing()

    eda.report(save_plots=True)     # the old "run everything at once" path
"""
from __future__ import annotations

import pandas as pd

from .schema import SchemaDetector
from .quality import QualityAnalyzer
from .profiler import StatisticalProfiler
from .visualizer import Visualizer


class EDA:
    def __init__(self, df: pd.DataFrame, output_dir: str = "eda_plots"):
        if not isinstance(df, pd.DataFrame):
            raise TypeError("EDA expects a pandas DataFrame.")
        self.df = df
        self.output_dir = output_dir

        # Lazy caches — nothing heavy runs until you ask for it.
        self._schema: dict | None = None
        self._quality: dict | None = None
        self._stats: dict | None = None
        self._viz: Visualizer | None = None

    # ===================================================================
    # Schema (computed once, then cached)
    # ===================================================================
    @property
    def schema(self) -> dict:
        if self._schema is None:
            self._schema = SchemaDetector(self.df).detect()
        return self._schema

    def columns(self, kind: str) -> list:
        """Columns of a given primary type ('numerical', 'categorical', ...)
        or property ('high_cardinality', 'constant', 'id_or_key')."""
        types = self.schema["primary_types"]
        props = self.schema["properties"]
        if kind in types:
            return list(types[kind])  #list returns a separate object avoids corruption of internal_schema
        if kind in props:
            return list(props[kind])
        valid = list(types) + list(props)
        raise KeyError(f"Unknown column kind '{kind}'. Choose from: {valid}")

    def refresh(self):
        """Drop every cache — call this if you mutate ``self.df`` in place."""
        self._schema = self._quality = self._stats = self._viz = None
        return self

    # ===================================================================
    # Quality  ->  DataFrames / dicts
    # ===================================================================
    @property
    def _quality_report(self) -> dict:
        if self._quality is None:
            self._quality = QualityAnalyzer(self.df, self.schema).analyze()
        return self._quality

    def missing(self) -> pd.DataFrame:
        """Per-column missing counts + percentages (columns with gaps only)."""
        data = self._quality_report["missing_values"]
        if not data: #handles errors when no missing values are present
            return pd.DataFrame(columns=["missing_count", "missing_pct"])
        out = (
            pd.DataFrame(data)
            .T.rename(columns={"count": "missing_count", "percentage": "missing_pct"})
            .sort_values("missing_pct", ascending=False)
        )
        return out

    def duplicates(self) -> dict:
        """Exact-duplicate count and any uniqueness violations on ID columns."""
        return self._quality_report["duplicates"]

    def data_gaps(self) -> pd.DataFrame:
        """Columns flagged as having critically high missingness."""
        gaps = self._quality_report["data_gaps"]
        return pd.DataFrame(gaps) if gaps else pd.DataFrame(columns=["column", "issue"])

    # ===================================================================
    # Statistical profiling  ->  DataFrames
    # ===================================================================
    @property
    def _stats_profile(self) -> dict:
        if self._stats is None:
            self._stats = StatisticalProfiler(self.df, self.schema).profile()
        return self._stats

    def describe_numeric(self) -> pd.DataFrame:
        """Mean/std/quartiles/skew/kurtosis for numerical columns (one row each)."""
        data = self._stats_profile["numerical_analysis"]
        return pd.DataFrame(data).T if data else pd.DataFrame()

    def describe_categorical(self) -> pd.DataFrame:
        """Cardinality + mode metrics for categorical columns (one row each)."""
        data = self._stats_profile["categorical_analysis"]
        if not data:
            return pd.DataFrame()
        # Keep scalar metrics in the table; the full top-5 dict stays available
        # through .category_distribution(col).
        rows = {c: {k: v for k, v in m.items() if k != "top_5_distribution"}
                for c, m in data.items()}
        return pd.DataFrame(rows).T

    def category_distribution(self, col: str) -> dict:
        """The top-5 value distribution captured for one categorical column."""
        data = self._stats_profile["categorical_analysis"]
        if col not in data:
            raise KeyError(f"'{col}' is not a profiled categorical column.")
        return data[col]["top_5_distribution"]

    def describe_boolean(self) -> pd.DataFrame:
        """Class balance (%) for boolean columns."""
        data = self._stats_profile["boolean_analysis"]
        if not data:
            return pd.DataFrame()
        rows = {c: m["class_percentages"] for c, m in data.items()}
        return pd.DataFrame(rows).T

    def value_counts(self, col: str, normalize: bool = False) -> pd.Series:
        """Thin pandas pass-through so you don't have to reach back to df."""
        return self.df[col].value_counts(normalize=normalize)

    def numeric_like(self) -> list:
        """Columns stored as text that *look* numeric ('500 sqft', '42 Lac').

        This is a diagnostic flag only — the engine deliberately does NOT clean
        them, because correct parsing (units, currency scale, sentinels) is
        dataset-specific. Convert them yourself with pandas, then re-run EDA on
        the cleaned frame to unlock numeric stats/correlation. For example:

            df["Carpet Area"] = df["Carpet Area"].str.extract(r"(\\d+\\.?\\d*)").astype(float)
        """
        return self.columns("numeric_like")

    def overview(self) -> pd.DataFrame:
        """One-row-per-column summary: dtype, detected type, nulls, uniques."""
        type_of = {}
        for t, cols in self.schema["primary_types"].items():
            for c in cols:
                type_of[c] = t
        rows = []
        for c in self.df.columns:
            rows.append({
                "dtype": str(self.df[c].dtype),
                "detected_type": type_of.get(c, "—"),
                "n_unique": int(self.df[c].nunique(dropna=True)),
                "null_pct": round(float(self.df[c].isnull().mean() * 100), 2),
            })
        return pd.DataFrame(rows, index=self.df.columns)

    # ===================================================================
    # Visualization  ->  Matplotlib Figures (render inline; save optional)
    # ===================================================================
    @property
    def viz(self) -> Visualizer:
        if self._viz is None:
            self._viz = Visualizer(self.df, self.schema, output_dir=self.output_dir)
        return self._viz

    def plot_distribution(self, col: str, save: bool = False):
        """Histogram+KDE and boxplot for a numerical column."""
        return self.viz.plot_numerical(col, save=save)

    def plot_counts(self, col: str, save: bool = False, top_n: int = 10):
        """Top-N category counts for a categorical column."""
        return self.viz.plot_categorical(col, save=save, top_n=top_n)

    def plot_correlation(self, save: bool = False, method: str = "pearson"):
        """Correlation heatmap across numerical columns."""
        return self.viz.plot_correlation(save=save, method=method)

    def plot_missing(self, save: bool = False):
        """Bar chart of missingness per column."""
        return self.viz.plot_missing(save=save)

    # ===================================================================
    # Convenience: the original "run everything at once" path
    # ===================================================================
    def report(self, save_plots: bool = True) -> dict:
        """Run the full pipeline and return every result in one dict.

        Equivalent to the old ``EDAEngine.run_full_pipeline()`` — handy for a
        quick first pass, but everything it produces is reachable à la carte
        through the individual methods above.
        """
        result = {
            "schema": self.schema,
            "quality": self._quality_report,
            "statistics": self._stats_profile,
        }
        if save_plots:
            self.viz.generate_all_plots(save=True)
            result["plots_dir"] = self.output_dir
        return result

    def __repr__(self) -> str:
        r, c = self.df.shape
        return f"<EDA: {r} rows × {c} cols  (call .overview() for a column summary)>"

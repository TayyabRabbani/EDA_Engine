# eda_engine/visualizer.py
import os
import pandas as pd
import seaborn as sns
import matplotlib.pyplot as plt


class Visualizer:
    """
    Schema-driven plotting engine.

    Every plot method *returns* the Matplotlib Figure (like calling a plotting
    helper yourself), so you can keep tweaking it. Nothing is forced to disk and
    no global backend is hijacked: in a notebook the figure renders inline; pass
    ``save=True`` to also write a PNG into ``output_dir``.
    """

    def __init__(self, df: pd.DataFrame, schema: dict, output_dir: str = "eda_plots"):
        self.df = df
        self.schema = schema
        self.output_dir = output_dir
        sns.set_theme(style="whitegrid")

    # ------------------------------------------------------------------ helpers
    def _finish(self, fig, filename: str | None, save: bool):
        """Optionally save, then detach from pyplot so the figure displays once."""
        fig.tight_layout()
        if save and filename:
            os.makedirs(self.output_dir, exist_ok=True)
            fig.savefig(os.path.join(self.output_dir, filename), dpi=150, bbox_inches="tight")

        # Detach means the *only* render is the returned figure's repr,
        # which avoids the inline backend showing it twice.
        plt.close(fig)
        return fig

    # ------------------------------------------------------------------ numeric
    def plot_numerical(self, col: str, save: bool = False):
        """Histogram + KDE next to a boxplot for a single continuous column."""
        if col not in self.df.columns:
            raise KeyError(f"Column '{col}' not in DataFrame.")

        fig, axes = plt.subplots(1, 2, figsize=(14, 5))
        sns.histplot(data=self.df, x=col, kde=True, ax=axes[0], color="skyblue")
        axes[0].set_title(f"{col} - Distribution & Density")
        sns.boxplot(data=self.df, x=col, ax=axes[1], color="salmon")
        axes[1].set_title(f"{col} - Outlier Profile (Boxplot)")
        return self._finish(fig, f"numerical_{col}.png", save)

    # -------------------------------------------------------------- categorical
    def plot_categorical(self, col: str, save: bool = False, top_n: int = 10):
        """Horizontal count plot of the top categories for a single column."""
        if col not in self.df.columns:
            raise KeyError(f"Column '{col}' not in DataFrame.")

        fig, ax = plt.subplots(figsize=(8, 5))
        order = self.df[col].value_counts().index[:top_n]
        sns.countplot(data=self.df, y=col, order=order, ax=ax,
                      palette="viridis", hue=col, legend=False)
        ax.set_title(f"{col} - Top {top_n} Category Counts")
        ax.set_xlabel("Count")
        ax.set_ylabel(col)
        return self._finish(fig, f"categorical_{col}.png", save)

    # -------------------------------------------------------------- correlation
    def plot_correlation(self, save: bool = False, method: str = "pearson"):
        """Correlation heatmap across the schema's numerical columns."""
        num_cols = [c for c in self.schema["primary_types"]["numerical"] if c in self.df.columns]
        if len(num_cols) < 2:
            raise ValueError("Need at least 2 numerical columns for a correlation matrix.")

        fig, ax = plt.subplots(figsize=(8, 6))
        corr_matrix = self.df[num_cols].corr(method=method)
        sns.heatmap(corr_matrix, annot=True, cmap="coolwarm", fmt=".2f",
                    linewidths=0.5, ax=ax, vmin=-1, vmax=1)
        ax.set_title(f"Numerical Correlation Matrix ({method.title()})")
        return self._finish(fig, "numerical_correlation.png", save)

    # ----------------------------------------------------------------- missing
    def plot_missing(self, save: bool = False):
        """Bar chart of missing-value percentage per column (columns with gaps)."""
        pct = (self.df.isnull().mean() * 100).sort_values(ascending=False)
        pct = pct[pct > 0]
        if pct.empty:
            raise ValueError("No missing values to plot.")

        fig, ax = plt.subplots(figsize=(8, max(3, 0.4 * len(pct))))
        sns.barplot(x=pct.values, y=pct.index, ax=ax, hue=pct.index,
                    palette="rocket", legend=False)
        ax.set_title("Missing Values by Column")
        ax.set_xlabel("% Missing")
        return self._finish(fig, "missing_values.png", save)

    # ------------------------------------------------------------ bulk pipeline
    def generate_all_plots(self, save: bool = True) -> list:
        """Old all-at-once behaviour: plot everything the schema supports.

        Returns the list of figures (and writes PNGs when ``save=True``).
        """
        figs = []
        for col in self.schema["primary_types"]["numerical"]:
            if col in self.df.columns:
                figs.append(self.plot_numerical(col, save=save))

        high_card = set(self.schema["properties"].get("high_cardinality", []))
        for col in self.schema["primary_types"]["categorical"]:
            if col in self.df.columns and col not in high_card:
                figs.append(self.plot_categorical(col, save=save))

        if len([c for c in self.schema["primary_types"]["numerical"] if c in self.df.columns]) >= 2:
            figs.append(self.plot_correlation(save=save))

        return figs

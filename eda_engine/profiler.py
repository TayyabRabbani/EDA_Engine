# eda_engine/profiler.py
import pandas as pd


class StatisticalProfiler:
    """
    Generates targeted mathematical and statistical profiles for variables
    based on their parsed primary schema types.
    """

    def __init__(self, df: pd.DataFrame, schema: dict):
        self.df = df
        self.schema = schema

    def profile(self) -> dict:
        return {
            "numerical_analysis": self._profile_numerical(),
            "categorical_analysis": self._profile_categorical(),
            "boolean_analysis": self._profile_boolean()
        }

    def _profile_numerical(self) -> dict:
        """Computes structural and distribution math for continuous variables."""
        numerical_cols = self.schema["primary_types"]["numerical"]
        analysis = {}

        for col in numerical_cols:
            if col in self.df.columns:
                series = self.df[col].dropna()
                if series.empty:
                    continue

                desc = series.describe()

                # IQR-based outlier fencing (Tukey): values outside
                # [Q1 - 1.5*IQR, Q3 + 1.5*IQR] are flagged.
                q1, q3 = float(desc["25%"]), float(desc["75%"])
                iqr = q3 - q1
                lower, upper = q1 - 1.5 * iqr, q3 + 1.5 * iqr
                outliers = series[(series < lower) | (series > upper)]
                total = len(series)

                analysis[col] = {
                    "mean": round(float(desc["mean"]), 3),
                    "std_dev": round(float(desc["std"]), 3),
                    "min": float(desc["min"]),
                    "25%": q1,
                    "50%_median": float(desc["50%"]),
                    "75%": q3,
                    "max": float(desc["max"]),
                    "variance": round(float(series.var()), 3),
                    "skewness": round(float(series.skew()), 3),
                    "kurtosis": round(float(series.kurt()), 3),
                    # --- robustness / validity signals ---
                    "outlier_count": int(len(outliers)),
                    "outlier_%": round(len(outliers) / total * 100, 2) if total else 0.0,
                    "n_zeros": int((series == 0).sum()),
                    "n_negative": int((series < 0).sum()),
                }
        return analysis

    def _profile_categorical(self) -> dict:
        """Computes cardinality profiles and class distributions for categorical features."""
        categorical_cols = self.schema["primary_types"]["categorical"]
        analysis = {}

        for col in categorical_cols:
            if col in self.df.columns:
                series = self.df[col].dropna()
                if series.empty:
                    continue

                # Skip deep value-count lookups for high cardinality text masks (like Cabin/Ticket)
                # to save memory/output bloating, but keep basic card metrics
                is_high_card = col in self.schema["properties"].get("high_cardinality", [])

                total_valid = len(series)
                value_counts = series.value_counts()
                mode_value = value_counts.index[0]
                mode_freq = int(value_counts.iloc[0])

                analysis[col] = {
                    "distinct_values": len(value_counts),
                    "mode": mode_value,
                    "mode_frequency": mode_freq,
                    "mode_percentage": round((mode_freq / total_valid) * 100, 2) if total_valid > 0 else 0.0,
                    # Top 5 distribution breakdowns only if it's manageable cardinality
                    "top_5_distribution": value_counts.head(
                        5).to_dict() if not is_high_card else "High Cardinality (Suppressed Distribution)"
                }
        return analysis

    def _profile_boolean(self) -> dict:
        """Calculates balance metrics for binary/boolean flags."""
        boolean_cols = self.schema["primary_types"]["boolean"]
        analysis = {}

        for col in boolean_cols:
            if col in self.df.columns:
                series = self.df[col].dropna()
                if series.empty:
                    continue

                # Inspect Class Imbalance
                normalized_map = series.value_counts(normalize=True).to_dict()

                # Turn keys into clean strings to handle variations safely
                #Converted to str because 1,0 and yes,no showed different behaviour
                clean_map = {str(k): round(float(v) * 100, 2) for k, v in normalized_map.items()}

                analysis[col] = {
                    "class_percentages": clean_map
                }
        return analysis
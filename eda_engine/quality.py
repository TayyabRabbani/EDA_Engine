# eda_engine/quality.py
import pandas as pd


class QualityAnalyzer:
    """
    Analyzes missing values, duplicate rows, and structural gaps
    in a DataFrame based on its structural schema properties.
    """

    def __init__(self, df: pd.DataFrame, schema: dict):
        self.df = df
        self.schema = schema
        self.n_rows = len(df)

    def analyze(self) -> dict:
        missing = self._analyze_missing()  # compute once, reuse for gap flagging
        return {
            "missing_values": missing,
            "duplicates": self._analyze_duplicates(),
            "data_gaps": self._flag_severe_gaps(missing)
        }

    def _analyze_missing(self) -> dict:
        """Calculates total missing values and percentages per column."""
        missing_counts = self.df.isnull().sum()

        # Also catch hidden text missing values (like empty strings or whitespaces)
        # for text/categorical data
        text_cols = self.schema["primary_types"]["text"] + self.schema["primary_types"]["categorical"]

        missing_summary = {}
        for col in self.df.columns:
            count = int(missing_counts[col])

            # Check for empty strings if the column is string-based
            if col in text_cols:
                empty_strings = int((self.df[col].astype(str).str.strip() == "").sum())
                count += empty_strings

            percentage = round((count / self.n_rows) * 100, 2) if self.n_rows > 0 else 0.0

            if count > 0:
                missing_summary[col] = {
                    "count": count,
                    "percentage": percentage
                }

        return missing_summary

    def _analyze_duplicates(self) -> dict:
        """Analyzes exact duplicates and key constraints."""
        total_exact_duplicates = int(self.df.duplicated().sum())

        summary = {
            "total_exact_row_duplicates": total_exact_duplicates,
            "key_violations": {}
        }   

        # Check if identified primary IDs are actually unique
        id_cols = self.schema["properties"].get("id_or_key", [])
        for col in id_cols:
            if col in self.df.columns:
                duplicated_keys = int(self.df.duplicated(subset=[col]).sum())
                if duplicated_keys > 0:
                    summary["key_violations"][col] = duplicated_keys

        return summary

    def _flag_severe_gaps(self, missing_info: dict, missing_threshold: float = 50.0) -> list:
        """Flags columns that have an alarming amount of missing data."""
        gaps = []
        for col, metrics in missing_info.items():
            if metrics["percentage"] >= missing_threshold:
                gaps.append({
                    "column": col,
                    "issue": f"Critically high missing data ({metrics['percentage']}%). Consider dropping."
                })
        return gaps
import re
import warnings
import pandas as pd


class SchemaDetector:
    """
    Generalized schema detector for automated EDA workflows.
    Separates columns into mutually exclusive primary types and applies property flags.
    """

    def __init__(self, df: pd.DataFrame):
        if df.empty:
            raise ValueError("The provided DataFrame is empty.")
        self.df = df
        self.n_rows = len(df)

    def detect(self) -> dict:
        # Separate primary types from behavioral properties
        schema = {
            "primary_types": {
                "numerical": [],
                "categorical": [],
                "text": [],
                "datetime": [],
                "boolean": [],
            },
            "properties": {
                "high_cardinality": [],
                "constant": [],
                "id_or_key": [],
                "numeric_like": [],  # object cols that are really numbers in disguise
            }
        }
        for col in self.df.columns:
            series = self.df[col]
            n_unique = series.nunique(dropna=True)  #number of unique values in a Pandas Series.
            unique_ratio = n_unique / self.n_rows if self.n_rows > 0 else 0

            # Near-unique columns may be identifiers/primary key
            # a continuous float (price, area, sensor reading) is also near-unique,
            # yet it's not PK.
            # near-unique columns are treated as IDs/PK for now. Its checked for continuous float later.
            near_unique = (n_unique == self.n_rows) or (unique_ratio > 0.95)

            if near_unique:
                if pd.api.types.is_numeric_dtype(series):  # checks for int32,int64 and float32,float64
                    nonnull = series.dropna()
                    is_int_like = (
                        pd.api.types.is_integer_dtype(series) #handles pure int values
                        or (len(nonnull) > 0 and (nonnull % 1 == 0).all()) #handles int disguised as float [1.0,2.0]
                    )
                    if is_int_like:
                        schema["properties"]["id_or_key"].append(col)
                        continue
                    # else: continuous float -> keep as a real numerical feature
                else:
                    schema["primary_types"]["text"].append(col)  # unique values like Names
                    continue

            # 1. Constant Column Check i.e A useless column
            if n_unique <= 1:
                schema["properties"]["constant"].append(col)
                # We still want to give it a base structural type, or we can choose to skip.
                # Usually best to categorize it, but keeping it out of primary prevents processing errors.
                continue

            # 2. Boolean Detection
            if self._is_boolean(series):
                schema["primary_types"]["boolean"].append(col)
                continue

            # 3. Datetime Detection (Check before text/categorical)
            if self._is_datetime(series):
                schema["primary_types"]["datetime"].append(col)
                continue

            # 4. Numerical Detection
            #  Refines the numerical block:
            if pd.api.types.is_numeric_dtype(series):
                # Check if it behaves like a discrete integer category
                nonnull = series.dropna()
                is_integer_type = pd.api.types.is_integer_dtype(series) or (
                    len(nonnull) > 0 and (nonnull % 1 == 0).all()
                )

                if is_integer_type and n_unique <= 10:  # Threshold of 10 unique integer values
                    schema["primary_types"]["categorical"].append(col)
                else:
                    schema["primary_types"]["numerical"].append(col)
                continue

            # 5. Text Detection (Unstructured long text vs short categories)
            if self._is_text(series):
                schema["primary_types"]["text"].append(col)
                if self._is_high_cardinality(n_unique, unique_ratio):
                    schema["properties"]["high_cardinality"].append(col)
                continue

            # 6. Categorical Fallback
            schema["primary_types"]["categorical"].append(col)
            if self._is_high_cardinality(n_unique, unique_ratio):
                schema["properties"]["high_cardinality"].append(col)

        # Post-pass: flag categorical columns that are really numbers wearing a
        # text costume (units, currency words, "x out of y"). They stay
        # categorical, but the flag tells you they're worth coercing.
        for col in schema["primary_types"]["categorical"]:
            if self._is_numeric_like(self.df[col]):
                schema["properties"]["numeric_like"].append(col)

        return schema

    # ======================================
    # Helper Methods
    # ======================================

    def _is_boolean(self, series: pd.Series) -> bool:
        if pd.api.types.is_bool_dtype(series):
            return True

        # Extract unique strings safely
        unique_values = set(str(x).strip().lower() for x in series.dropna().unique())

        if not unique_values:
            return False

        # Use subset checking so single-value columns (e.g., only "Yes") still trigger true
        valid_patterns = [{"0", "1"}, {"true", "false"}, {"yes", "no"}]
        return any(unique_values.issubset(pattern) for pattern in valid_patterns)

    def _is_datetime(self, series: pd.Series) -> bool:
        # If it's already a datetime dtype, jump out early
        if pd.api.types.is_datetime64_any_dtype(series):
            return True

        if not pd.api.types.is_object_dtype(series):
            return False

        sample = series.dropna().head(20).astype(str)
        if sample.empty:
            return False

        success_count = 0
        attempted = 0
        with warnings.catch_warnings():
            warnings.simplefilter("ignore")
            for value in sample:
                # Avoid trying to parse pure numerical strings as dates (e.g., "100000")
                if value.isdigit() and len(value) != 8:
                    continue
                attempted += 1
                try:
                    pd.to_datetime(value, errors='raise', format='mixed')
                    success_count += 1
                except (ValueError, TypeError, OverflowError):
                    pass

        # Divide by what we actually tried to parse, not the whole sample,
        # so skipped numeric strings don't sink an otherwise-valid date column.
        return attempted > 0 and (success_count / attempted) > 0.8

    def _is_text(self, series: pd.Series) -> bool:
        if not pd.api.types.is_object_dtype(series):
            return False

        # Dropna and convert to avoid attribute errors
        clean_series = series.dropna().astype(str)
        if clean_series.empty:
            return False

        # Sampling massive datasets speeds this up massively
        sample_series = clean_series.sample(min(100, len(clean_series)), random_state=42)

        avg_length = sample_series.str.len().mean()
        avg_word_count = sample_series.str.split().str.len().mean()

        return avg_length > 50 or avg_word_count > 7

    def _is_high_cardinality(self, n_unique: int, unique_ratio: float) -> bool:
        # High cardinality threshold: arbitrary but 30% or more than 50 distinct items works well
        return unique_ratio > 0.30 or n_unique > 50

    def _is_numeric_like(self, series: pd.Series) -> bool:
        """True if an object column *looks like* numbers wearing a text costume —
        i.e. most values start with a digit (optionally a >/</~ comparator):
        '500 sqft', '42 Lac', '> 10', '10 out of 11'.

        This is a purely structural FLAG, on purpose. It does NOT parse units,
        currency, or sentinels — how to turn '42 Lac' into 4_200_000 is
        dataset-specific knowledge that belongs in your own pandas cleaning,
        not in a generic helper.
        """
        if not pd.api.types.is_object_dtype(series):
            return False
        clean = series.dropna().astype(str)
        if clean.empty:
            return False
        sample = clean.sample(min(200, len(clean)), random_state=42)
        starts_numeric = sample.str.match(r"^\s*[<>~]?\s*-?\d")  #
        return starts_numeric.mean() > 0.8  #avg of booleans
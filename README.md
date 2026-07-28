# EDA Engine 🔍

A **schema-driven, on-demand Exploratory Data Analysis (EDA) engine** designed to automate repetitive profiling, data quality checks, and visualization tasks for data analysts and machine learning practitioners.

Instead of repeatedly writing boilerplate **Pandas**, **Matplotlib**, and **Seaborn** code for every dataset, **EDA Engine** acts as a smart facade that automatically:

* Detects dataset schemas
* Flags structural issues and data quality risks
* Generates mathematical/statistical profiles
* Produces ready-to-use visualizations
* Supports modular, lazy-loaded analysis workflows

The engine is designed to feel familiar to **Pandas users** while significantly reducing repetitive analysis code.

---

##  Features

### 📊 Automatic Schema Detection

Automatically classifies columns into:

* Numerical
* Categorical
* Text
* Boolean
* Datetime

It also identifies behavioral metadata such as:

* `high_cardinality`
* `constant`
* `id_or_key`
* sparse/missing-heavy columns

---

###  Data Quality Analysis

Quickly identify:

* ✅ Missing values
* ✅ Duplicate rows
* ✅ Primary key violations
* ✅ Data gaps (high null percentage)
* ✅ Structural inconsistencies

---

###  Statistical Profiling

Generate rich summaries for:

#### Numerical Features

* Mean
* Median
* Standard deviation
* Variance
* Skewness
* Kurtosis
* IQR-based outlier detection

#### Categorical Features

* Unique counts
* Mode
* Frequency distribution

#### Boolean Features

* Exact class balance ratios

---

###  Built-in Visualizations

Generate inline charts instantly:

* Histograms + KDE
* Boxplots
* Correlation heatmaps
* Missing value plots
* Category frequency charts

All plots can optionally be saved to disk.

##  Installation

### Clone the repository

```bash
git clone https://github.com/yourusername/eda-engine.git
cd eda-engine
```

### Install dependencies

Using pip:

```bash
pip install -r requirements.txt
```

## Quick Start

The main entry point is the `EDA` class.

Initialize it once with a Pandas DataFrame and call only the analysis methods you need.

```python
import pandas as pd
from eda_engine import EDA

# Load dataset
df = pd.read_csv("your_dataset.csv")

# Initialize engine
eda = EDA(df)

# Get structural overview
print(eda.overview())

# Missing values
print(eda.missing())

# Statistical profiling
print(eda.describe_numeric())

# Correlation heatmap
eda.plot_correlation()

# Full automated report
eda.report(save_plots=True)
```

---

# 📖 API Reference

The engine is **modular and lazy-loaded** — expensive computations only run when explicitly requested.

---

## 1. Structural & Quality Checks

### `eda.overview()`

Returns a DataFrame summarizing:

* Column name
* Data type
* Detected schema type
* Unique values
* Missing percentage
---

### `eda.missing()`

Returns columns containing missing values sorted by null percentage.

---

### `eda.duplicates()`

Checks:

* Exact duplicate rows
* Primary key violations

Example output:

```python
{
    "duplicate_rows": 42,
    "primary_key_violations": {
        "PassengerId": 3
    }
}
```

---

### `eda.data_gaps()`

Flags columns with **critical missing data (≥ 50%)**.

Useful for deciding whether to drop features.

---

### `eda.schema`

Returns the internal schema classification dictionary.

Example:

```python
{
    "numerical": ["Age", "Fare"],
    "categorical": ["Sex", "Embarked"],
    "text": ["Name"],
    "boolean": ["Survived"],
    "datetime": [],
    "high_cardinality": ["Ticket"],
    "id_or_key": ["PassengerId"]
}
```

---

## 2. Statistical Profiling

### `eda.describe_numeric()`

Generates advanced numerical statistics.

Includes:

* Mean
* Median
* Variance
* Standard deviation
* Skewness
* Kurtosis
* Outlier counts (Tukey IQR)

---

### `eda.describe_categorical()`

Profiles categorical variables.

Includes:

* Distinct values
* Mode
* Frequency

---

### `eda.describe_boolean()`

Shows exact class balance.

Example:

| Class | Count | Percentage |
| ----- | ----- | ---------- |
| True  | 620   | 62%        |
| False | 380   | 38%        |

---

### `eda.value_counts(column_name)`

Convenience wrapper around Pandas value counts.

---

## 3. Visualization Methods

All plotting methods return a **Matplotlib Figure object** and render inline automatically.

You can optionally save plots using:

```python
save=True
```

---

### Distribution Plot

### `eda.plot_distribution(column_name)`

Creates:

* Histogram
* KDE curve
* Boxplot

Useful for understanding distributions and spotting outliers.

```python
eda.plot_distribution("Age")
```

---

### Count Plot

### `eda.plot_counts(column_name, top_n=10)`

Displays category frequencies.

```python
eda.plot_counts("Embarked")
```

---

### Correlation Heatmap

### `eda.plot_correlation(method="pearson")`

Generates correlation heatmap for numerical features.

```python
eda.plot_correlation()
```

Supported methods:

* `"pearson"`
* `"spearman"`
* `"kendall"`

---

### Missing Values Plot

### `eda.plot_missing()`

Visualizes missing data severity across columns.

```python
eda.plot_missing()
```

---

## 4. Bulk Execution

### `eda.report(save_plots=True)`

Runs the **complete EDA pipeline** end-to-end.

Returns:

* Structural overview
* Missing value analysis
* Duplicate checks
* Statistical summaries
* Visualizations

```python
report = eda.report(save_plots=True)
```

Example:

```python
report.keys()

dict_keys([
    'overview',
    'missing',
    'duplicates',
    'numeric_profile',
    'categorical_profile',
    'boolean_profile'
])
```
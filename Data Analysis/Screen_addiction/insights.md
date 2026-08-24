# Screen Addiction & User Habit Profiling

An exploratory data analysis (EDA) of a screen time dataset using **EDAEngine**, a custom Python package for automated data profiling, statistical analysis, visualization, and quality assessment.

The objective of this project is to understand the correlation between screen time metrics and digital addiction, utilizing an XGBoost model to evaluate the predictive power of selected features.

---

# Dataset Overview

The dataset contains nearly **691,000 user records**, providing robust large-scale insights into screen time behaviors.

## Selected Feature Categories

This analysis focuses on the specific numerical features that are strong indicators of screen addiction:
- **Daily Screen Time Hours** (`daily_screen_time_hours`)
- **Social Media Hours** (`social_media_hours`)
- **Gaming Hours** (`gaming_hours`)
- **Work/Study Hours** (`work_study_hours`)
- **Weekend Screen Time** (`weekend_screen_time`)

### Target Variable
- **Addiction Label** (`addicted_label`)

---

# Automated EDA Pipeline

This analysis was generated using **EDAEngine**, which automatically performs:

- Schema Detection
- Data Type Classification
- Missing Value Analysis
- Duplicate Detection
- Numerical Profiling
- Categorical Frequency Analysis
- Boolean Feature Analysis
- Distribution Visualization
- Outlier Detection
- Automated JSON Report Generation

---

# Target Distribution

| Label | Meaning | Percentage |
|---------|---------|-----------:|
| 1 | Addicted | **70.94%** |
| 0 | Not Addicted | **29.06%** |

### Observation

The dataset is somewhat imbalanced, with a significant majority (~71%) classified as experiencing digital addiction based on their labels. However, this is sufficient to train a robust binary classification model.

---

# Key Selected Indicators Analysis

## Daily Screen Time Hours (`daily_screen_time_hours`)

| Statistic | Value |
|-----------|-------:|
| Mean | **7.64 hours** |
| Median | 7.77 hours |
| Maximum | 15.0 hours |
| Missing | ~13.86% |

**Observations**
- A highly significant feature where the average user spends ~7.6 hours per day on screens.
- Distribution implies consistent daily usage.

## Weekend Screen Time (`weekend_screen_time`)

| Statistic | Value |
|-----------|-------:|
| Mean | **9.48 hours** |
| Median | 9.58 hours |
| Maximum | 17.56 hours |
| Missing | ~16.21% |

**Observations**
- Screen time spikes dramatically during weekends compared to regular daily usage.
- An average of almost 9.5 hours highlights recreational reliance.

## Social Media Hours (`social_media_hours`)

| Statistic | Value |
|-----------|-------:|
| Mean | **2.47 hours** |
| Median | 2.31 hours |
| Maximum | 8.0 hours |
| Missing | ~19.38% |

**Observations**
- Users spend significant continuous blocks of time on social media platforms.
- Over 1,200 mild statistical outliers indicate extreme social media usage by a subset of users.

## Work/Study Hours & Gaming Hours

- **Work/Study Hours (`work_study_hours`)**: Averages 2.36 hours. Has moderate missing values (~7.45%).
- **Gaming Hours (`gaming_hours`)**: Averages 1.46 hours. Missing in ~18.34% of records.

---

# XGBoost Predictive Modeling

To showcase the ability of the EDA engine and advanced data analysis skills, an **XGBoost Classifier** was trained using exclusively the selected core features mentioned above to classify the `addicted_label`. 

The model was trained on an 80/20 train-validation split without requiring prior data imputation, utilizing XGBoost's native handling of missing values.

## Performance Metrics

| Metric | Score |
|---------|--------|
| **ROC-AUC** | **0.9427** |
| **Accuracy** | **87.04%** |

### Classification Report

| Class | Precision | Recall | F1-Score | Support |
|-------|-----------|--------|----------|---------|
| **0 (Not Addicted)** | 0.80 | 0.74 | 0.77 | 40,179 |
| **1 (Addicted)** | 0.90 | 0.92 | 0.91 | 98,095 |
| **Macro Avg** | 0.85 | 0.83 | 0.84 | 138,274 |

### Observations on Model Performance

The XGBoost model demonstrates outstanding predictive power (ROC-AUC > 0.94) using only five core numerical features. It successfully handles the class imbalance natively, exhibiting a strong 0.92 recall and 0.90 precision for the dominant 'Addicted' class.

---

# Feature Importance Insights

Analysis of the model's feature importance (Gain/Weight) reveals the strongest indicators of screen addiction among the selected variables:

| Feature | Importance Score | Impact Level |
|---------|------------------:|-------------|
| **Daily Screen Time Hours** | **0.4513** | 🔥 Very Strong |
| **Weekend Screen Time** | **0.2402** | ⚡ Strong |
| **Social Media Hours** | **0.2315** | ⚡ Strong |
| **Work/Study Hours** | 0.0409 | 📉 Weak |
| **Gaming Hours** | 0.0361 | 📉 Weak |

## 💡 Why are these features strong indicators?

1. **Daily Screen Time (Score: 0.451):** The absolute strongest indicator. Prolonged exposure across the entire day correlates directly with digital dependency, irrespective of the specific application. This foundational metric encapsulates the user's overall digital lifestyle.
2. **Weekend Screen Time (Score: 0.240):** High weekend usage acts as a critical signal of recreational dependency. When structured work or study obligations diminish during weekends, sustained high screen time reveals habitual and potentially compulsive digital consumption.
3. **Social Media Hours (Score: 0.231):** Social platforms are inherently designed to maximize retention and exploit feedback loops (e.g., dopamine hits). Extended hours spent here strongly correlate with behavioral addiction patterns, distinguishing purely productive screen use from compulsive scrolling.
4. **Work/Study & Gaming Hours:** Interestingly, these provided much lower predictive value in this specific context compared to overall daily aggregates and social media. Productive screen time (`work_study`) doesn't directly imply an unhealthy dependency, explaining its low contribution to the addiction label.

---

# Conclusion

The analysis validates the effectiveness of **EDAEngine** in profiling massive datasets (nearly 700k records) rapidly. We demonstrated that digital addiction can be highly predictably modeled (ROC-AUC ~0.94) by isolating a few core screen time metrics. Notably, total aggregate screen time (both daily and on weekends) paired with social media consumption act as the definitive markers of digital dependency, far outweighing the impact of productive work or gaming alone.

# HR Analytics: Comprehensive Exploratory and Predictive Analysis

This repository presents an end-to-end data analysis and machine learning pipeline for an **HR Analytics** dataset. The primary business objective is to understand the factors that drive employee attrition (whether an employee is looking for a new job) and to build a predictive model to identify flight risks.

---

## 1. Executive Summary
* **Baseline Attrition:** The workforce is moderately imbalanced, with **24.93%** of candidates actively looking for a job change.
* **Top Drivers of Attrition:** Living in a city with a lower development index and having less professional experience are the two strongest indicators of flight risk.
* **Predictive Success:** A tuned Random Forest Classifier was successfully deployed, achieving a **79% Recall** in identifying employees planning to leave.

---

## 2. Baseline Workforce Profile (Univariate EDA)
Initial automated exploratory data analysis revealed the core demographics of the dataset:
* **Experience & Education:** The dataset is dominated by highly experienced professionals (the largest group has >20 years of experience). Nearly **72%** have relevant industry experience, and **88%** come from STEM backgrounds.
* **Company Profile:** Private organizations (Pvt Ltd) account for **75%** of employers, with medium-sized organizations (50-500 employees) being the most common.
* **Demographics:** The workforce is heavily male-dominated (**90%**) and geographically concentrated in highly developed cities (median City Development Index of 0.903).

---

## 3. Data Engineering & Cleaning
To prepare the dataset for bivariate analysis and machine learning, significant data cleaning was performed:
* **Missing Value Imputation:** Employment-related attributes had up to 32% missing data (`company_type`, `company_size`). To preserve the dataset, these were safely imputed with "Unknown" and "Not_Applicable" labels rather than dropping rows.
* **String-to-Numeric Conversion:** Categorical text in numerical columns (e.g., `>20` and `<1` in `experience`) were cleaned and converted to continuous floats to allow for mathematical correlation.
* **Skewness Handling:** A logarithmic transformation was applied to `training_hours` to handle massive right-skewed outliers, and the `city_development_index` was binned for easier HR readability.

---

## 4. Key Drivers of Attrition (Bivariate Analysis)
By cross-referencing features against the `target` variable, we uncovered the "Why" behind employee turnover:

* **The Environment Factor:** Candidates in lower-development cities are significantly more likely to seek new jobs, likely looking for upward mobility or relocation.
* **The Experience Factor:** Junior to mid-level employees are the biggest flight risks as they chase salary bumps. Senior veterans (15-20+ years) are highly stable.
* **The Startup Squeeze:** Employees at Early Stage Startups and Funded Startups show noticeably higher attrition rates compared to those in Public Sector or large Enterprise roles.
* **The Training Paradox:** Density plots and correlation matrices reveal that `training_hours` has virtually zero correlation with attrition. Providing extensive training neither buys loyalty nor pushes employees to leave.

---

## 5. Predictive Modeling 
To move from analysis to proactive retention, we trained a **Random Forest Classifier** to predict which specific employees will leave.

* **Data Prep:** Redundant columns (`city`) were dropped, and categorical text was One-Hot Encoded to prevent the curse of dimensionality.
* **Handling Imbalance:** The model utilized `class_weight='balanced'` and pruned hyperparameters (`max_depth=8`, `min_samples_leaf=10`) to prevent overfitting.
* **Model Performance:** The model achieved an excellent **Recall of 79%** for the minority class (Leavers). In a business context, this means the model successfully identifies nearly 8 out of 10 employees who are secretly planning to quit.
* **Feature Importance:** The model mathematically confirmed our visual EDA: `city_development_index` and `experience` were ranked as the top two most important features for predicting a job change.

---

## 6. Strategic HR Recommendations
1. **Targeted Retention Budgets:** HR should focus retention bonuses and stay-interviews specifically on junior/mid-level employees living in lower-development cities.
2. **Hiring for Stability:** To reduce turnover in critical roles, prioritize hiring candidates from highly developed cities or those with 15+ years of experience.
3. **Re-evaluate Startup Culture:** If operating an Early Stage Startup, aggressive retention strategies are required, as this environment bleeds talent at a much higher rate than corporate peers.
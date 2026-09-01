# Global Data Science Salary Trends & Predictive Modeling

## Summary
This report presents a comprehensive analysis of the global data science job market, focusing on compensation trends and the development of a machine learning model to predict salaries. By analyzing over 2,500 unique salary records of data professionals, we identified the core drivers of compensation and engineered a highly optimized Ridge Regression model to estimate market rates.

---

## 1. Exploratory Data Analysis (EDA) Findings

Through rigorous visualization and statistical analysis, several key truths about the data science job market were uncovered:

* **The Experience Premium:** Experience is a strict, linear driver of compensation. There are clear, defined salary floor increases as professionals move from Entry-Level to Mid-Level, Senior, and ultimately Executive roles.
* **Geography Dictates Baseline Pay:** Company location is the single largest determinant of salary. Roles based in the United States command a massive premium over the rest of the global market. 
* **The Remote Work Landscape:** Fully remote and strictly on-site roles offer highly competitive and similar salary ranges. However, cross-border remote work (where the employee resides in a different country than the employer) creates unique pricing dynamics.
* **Salary Growth vs. Composition Shift:** While average salaries appeared to skyrocket between 2020 and 2023, much of this was driven by a composition shift in the industry (a much higher volume of US-based, Senior-level roles being hired and reported) rather than pure inflationary wage growth.

---

## 2. Predictive Modeling Strategy & Decisions

To move from historical analysis to active prediction, a machine learning pipeline was built. The following strategic decisions were made to ensure the model was honest, robust, and highly accurate:

* **Strict Data Integrity:** The dataset was rigorously deduplicated before splitting into training and testing sets. This prevented data leakage and ensured the model was evaluated on its ability to generalize, rather than its ability to memorize duplicate rows.
* **Targeting Proportional Error (Log-Transformation):** Instead of predicting raw dollar amounts, the model was designed to predict the *natural logarithm* of the salary. This allowed the model to optimize for **MAPE (Mean Absolute Percentage Error)**. In compensation analysis, promising an estimate "within 15% of actual pay" is vastly more useful than a flat dollar-amount error margin.
* **Feature Engineering:** High-cardinality text columns (like having over 90 unique job titles) were grouped into the Top 15 roles to prevent sparse matrices. Crucially, both `company_location` and `employee_residence` were preserved, and a `cross_border` flag was engineered to capture the nuance of international remote hiring.
* **Algorithm Selection (Ridge Regression):** While complex, non-linear algorithms (like Random Forest or XGBoost) are popular, testing revealed that compensation in this dataset follows a strictly additive, linear structure (e.g., Base Salary + Seniority Bump + US Location Premium). Therefore, **Ridge Regression** was selected. It outperformed complex tree-based models while remaining lightweight and mathematically interpretable.

---

## 3. Conclusion

The final Ridge Regression model achieves an **R² score of ~0.42**. While this number may initially seem modest, it is highly successful given the context of the dataset.


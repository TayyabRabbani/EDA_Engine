# Heart Attack Analysis: Step-by-Step Decisions

### Step 1: Check the Baseline
* **Action:** Reviewed the EDA engine's `Insights.md` report.
* **Findings:** The dataset is extremely small (303 rows) but incredibly clean. There are zero missing values. The target variable (`output`) is perfectly balanced (54% Heart Disease vs 45% No Heart Disease). There is exactly 1 duplicate record.
* **Decision:** Because medical data relies on precise biological metrics, we don't need to do heavy feature grouping. The data is almost ready to go as-is.

### Step 2: Clean and Organize
* **Decision 1:** Drop the 1 duplicate record.
    * *Reason:* As we learned from the Salary dataset, duplicate records cause "Data Leakage" where the model memorizes answers for the test exam. Even though it's only 1 row, we drop it to ensure strict mathematical honesty.
* **Decision 2:** No missing value imputation needed.
    * *Reason:* The dataset is pristine. No columns need to be dropped or filled.

### Step 3: Visual Storytelling (Bivariate Analysis)
* **Decision 1:** Density Plot of Age vs. Heart Disease.
    * *Reason:* We need to visually confirm if age is a primary driver. A density plot shows the "shape" of patient ages, letting us see exactly at what age heart disease diagnoses spike.
* **Decision 2:** Boxplot of Maximum Heart Rate (`thalachh`) vs. Heart Disease.
    * *Reason:* A boxplot will clearly show if patients diagnosed with heart disease generally have higher or lower maximum heart rates compared to healthy patients, mapping out the full biological range.
* **Decision 3:** Barplot of Chest Pain Type (`cp`) vs. Heart Disease.
    * *Reason:* Chest pain is the most common symptom, but the dataset categorizes it into 4 types. A bar chart will instantly show which specific type of chest pain is the highest indicator of a positive diagnosis.
* **Decision 4: Curation over Exhaustion (Why we didn't plot all 13 columns).**
    * *Reason:* In data science storytelling, plotting every single variable causes "chart fatigue" for the audience. We intentionally selected the 3 features with the highest intuitive medical relevance (Age, Heart Rate, Symptom/Pain). We skipped variables like `chol` (Cholesterol) because the EDA report showed it had a surprisingly weak correlation to the target. We skipped variables like `oldpeak` and `slp` because they are highly technical ECG readings that confuse non-medical audiences. (However, all 13 columns were kept for the Machine Learning model to evaluate).

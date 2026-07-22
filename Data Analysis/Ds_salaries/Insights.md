# Global Data Science Salaries Dataset Analysis

This project presents an exploratory analysis of the **Global Data Science Salaries** dataset. The dataset contains salary records for data professionals across different countries, company sizes, experience levels, employment types, and work arrangements. The objective of this analysis is to understand workforce composition, compensation trends, and the overall characteristics of the global data science job market.

---

## Dataset Summary

The dataset includes information such as:

- Salary (Local Currency)
- Salary (USD)
- Experience Level
- Employment Type
- Company Size
- Remote Work Ratio
- Company Location
- Employee Residence
- Job Title
- Salary Currency
- Work Year

---

# Key Insights

## Salary Distribution

### Local Currency Salaries

The `salary` column exhibits an extremely right-skewed distribution because salaries are reported in multiple currencies. Countries with high-denomination currencies contribute very large numerical values, making direct comparisons difficult.

**Summary Statistics**

| Metric | Value |
|--------|-------:|
| Mean | 190,695 |
| Median | 138,000 |
| Maximum | 30,400,000 |
| Outliers | 113 (3.01%) |

### Standardized USD Salaries

After converting salaries into USD, the distribution becomes significantly more representative of actual compensation levels.

| Metric | Value |
|--------|-------:|
| Mean | **$137,570** |
| Median | **$135,000** |
| Standard Deviation | **$63,056** |
| Maximum | **$450,000** |
| Outliers | **63 (1.68%)** |

Most salaries fall between **$95,000** and **$175,000**, indicating that the majority of professionals earn within this range.

---

## Experience Level Distribution

Senior professionals account for the majority of records.

| Experience Level | Count | Percentage |
|-----------------|------:|-----------:|
| Senior (SE) | 2,516 | **67.00%** |
| Mid-Level (MI) | 805 | 21.44% |
| Entry-Level (EN) | 320 | 8.52% |
| Executive (EX) | 114 | 3.03% |

**Observation**

The dataset is heavily skewed toward experienced professionals, suggesting that senior roles dominate hiring in the data science industry.

---

## Employment Type

| Employment Type | Count | Percentage |
|----------------|------:|-----------:|
| Full-Time (FT) | 3,718 | **99.01%** |
| Part-Time (PT) | 17 | 0.45% |
| Contract (CT) | 10 | 0.27% |
| Freelance (FL) | 10 | 0.27% |

**Observation**

Nearly every salary record corresponds to a full-time position, indicating that permanent employment is the predominant hiring model.

---

## Company Size

| Company Size | Count | Percentage |
|-------------|------:|-----------:|
| Medium (M) | 3,153 | **83.97%** |
| Large (L) | 454 | 12.09% |
| Small (S) | 148 | 3.94% |

**Observation**

Medium-sized organizations represent the largest share of employers in the dataset.

---

## Remote Work Distribution

| Remote Ratio | Count | Percentage |
|-------------|------:|-----------:|
| On-site (0%) | 1,923 | **51.21%** |
| Fully Remote (100%) | 1,643 | 43.75% |
| Hybrid (50%) | 189 | 5.03% |

**Observation**

On-site positions remain slightly more common than fully remote roles, while hybrid work arrangements account for a relatively small portion of jobs.

---

## Geographic Distribution

The dataset is heavily concentrated in the United States.

| Metric | Percentage |
|--------|-----------:|
| Companies Located in the US | **80.96%** |
| Employees Residing in the US | **80.00%** |

**Observation**

The dominance of US-based companies suggests that salary statistics largely reflect the U.S. data science market.

---

## Salary Currency

Although the dataset contains **20 different currencies**, most salaries are reported in only a few.

| Currency | Count | Percentage |
|----------|------:|-----------:|
| USD | 3,224 | **85.86%** |
| EUR | 236 | 6.28% |
| GBP | 161 | 4.29% |
| INR | 60 | 1.60% |
| CAD | 25 | 0.67% |

**Observation**

USD overwhelmingly dominates the dataset, reflecting the high proportion of salaries originating from the United States.

---

## Work Year Distribution

| Year | Records |
|------|--------:|
| 2023 | 1,785 |
| 2022 | 1,664 |
| 2021 | 230 |
| 2020 | 76 |

**Observation**

More than 90% of the records originate from **2022 and 2023**, making the dataset representative of recent hiring trends in the data science industry.

---

## Correlation Analysis

The Pearson correlation between `salary` (local currency) and `salary_in_usd` is approximately **-0.02**, indicating virtually no linear relationship.

This occurs because local salaries are reported in different currencies with varying exchange rates. As a result, standardized USD salaries provide a much more meaningful basis for comparison across countries.

---

# Overall Findings

- The dataset primarily represents the **2022–2023** data science job market.
- Senior professionals account for approximately **67%** of all salary records.
- Nearly **99%** of positions are full-time.
- Medium-sized companies dominate hiring activity.
- On-site and fully remote roles are both common, with hybrid roles being relatively uncommon.
- The United States accounts for the vast majority of companies and employees represented in the dataset.
- Salary comparisons are significantly more meaningful when using **salary_in_usd** rather than local currency values.
- Most standardized salaries fall between **$95K and $175K**, with only a small proportion of high-income outliers.

---

## Conclusion

The **Global Data Science Salaries** dataset provides valuable insights into compensation patterns, workforce demographics, company characteristics, and remote work trends across the data science industry. It highlights the dominance of senior full-time roles, the concentration of opportunities within the United States, and the importance of using standardized salary values for meaningful cross-country comparisons.
ESG & Profitability Dashboard

1. Problem & User
This project investigates whether companies with higher carbon emissions intensity tend to have lower profit margins, and how ESG environmental scores correlate with financial performance. The target users are ESG analysts, sustainability investors, and corporate managers seeking data‑driven insights into the trade‑off between environmental impact and profitability.

 2. Data
- Source : [ESG & Financial Performance Dataset](https://www.kaggle.com/datasets/shriyashjagtap/esg-and-financial-performance-dataset) (Kaggle)
- Access date : April 24, 2026
- Key fields:
  - Financial: ProfitMargin, Revenue, MarketCap, GrowthRate
  - Environmental: CarbonEmissions, WaterUsage, EnergyConsumption
  - ESG scores: ESG_Overall, ESG_Environmental, ESG_Social, ESG_Governance
  - Meta: CompanyID, CompanyName, Industry, Region, Year

3. Methods
(1) Data loading & cleaning – Load CSV, drop missing values, compute derived metrics
(2) Interactive dashboard – Built with Streamlit; provides multi‑select filters for industry, region, and year range.
(3) Visualizations – Created using Plotly:
- KPI cards (average profit margin, carbon intensity, ESG environmental score, water intensity)
- Customizable scatter plot (user selects X/Y axes and color grouping)
- Time‑series line charts (profit margin, carbon intensity, ESG environmental)
- Correlation heatmap of numerical features
- Box plots for profit margin and carbon intensity by industry
- Regional bar chart (profit margin colored by carbon intensity)
- Summary statistics table and raw data view with CSV download.

4. Key Findings
- Negative correlation between carbon intensity and profit margin (higher emitters tend to have lower margins) – visible in scatter plots and industry box plots.
- Technology and Healthcare industries show both low carbon intensity and high profit margins, while "Energy and Utilities" exhibit the opposite pattern.
- ESG Environmental score is moderately positively correlated with profit margin, suggesting that better environmental practices do not necessarily harm profitability.
- Water intensity varies widely across industries, with Manufacturing and Energy showing the highest values.
- Regional differences exist: North America and Europe have higher average profit margins but also higher carbon intensity compared to Asia and Africa.

5. How to run
streamlit run app.py

6. Demo
Demo video: https://youtu.be/your-video-link

7. Limitations & next steps
-Data limitations: The dataset is simulated, not real corporate data. Real‑world relationships might differ due to reporting biases.

-Simplified metrics: Carbon intensity is computed as emissions / revenue, ignoring differences in industry‑specific denominators

-Missing variables: The analysis does not control for company size, leverage, or R&D intensity, which could confound the observed correlations.

Next steps:

-Incorporate real‑world data from WRDS Trucost and Compustat.

-Add regress models to quantify the impact of carbon intensity on profit margin while controlling for other factors.

-Extend the dashboard with predictive "what‑if" scenarios and time‑series forecasting.

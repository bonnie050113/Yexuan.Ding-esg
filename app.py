import streamlit as st
import pandas as pd
import plotly.express as px
import plotly.graph_objects as go
import numpy as np

st.set_page_config(page_title="ESG & Profitability Dashboard", layout="wide")
st.title(" Advanced ESG & Financial Performance Analysis")
st.markdown("""
This interactive dashboard explores relationships between **carbon emissions intensity**, **ESG scores**, **profit margin**, and other financial metrics.
Data source: ESG & Financial Performance Dataset (Kaggle).
""")

@st.cache_data
def load_data():
    data_path = "cleaned_esg_data.csv"
    df = pd.read_csv(data_path)
    if 'CarbonIntensity' not in df.columns and 'CarbonEmissions' in df.columns and 'Revenue' in df.columns:
        df['CarbonIntensity'] = df['CarbonEmissions'] / df['Revenue']
    df['WaterIntensity'] = df['WaterUsage'] / df['Revenue']
    df['EnergyIntensity'] = df['EnergyConsumption'] / df['Revenue']
    return df

df = load_data()

st.sidebar.header("Filter Options")
industries = sorted(df['Industry'].dropna().unique())
selected_industries = st.sidebar.multiselect("Select Industry", industries, default=industries[:3])

min_year, max_year = int(df['Year'].min()), int(df['Year'].max())
year_range = st.sidebar.slider("Select Year Range", min_year, max_year, (min_year, max_year))

regions = sorted(df['Region'].dropna().unique())
selected_regions = st.sidebar.multiselect("Select Region", regions, default=regions)

filtered = df[
    (df['Industry'].isin(selected_industries)) &
    (df['Year'].between(year_range[0], year_range[1])) &
    (df['Region'].isin(selected_regions))
]

if filtered.empty:
    st.warning("No data matches the current filters. Please adjust.")
    st.stop()

col1, col2, col3, col4 = st.columns(4)
with col1:
    avg_margin = filtered['ProfitMargin'].mean()
    st.metric(" Avg Profit Margin", f"{avg_margin:.1f}%")
with col2:
    avg_intensity = filtered['CarbonIntensity'].mean()
    st.metric(" Avg Carbon Intensity", f"{avg_intensity:.2f} tons/$M")
with col3:
    avg_esg = filtered['ESG_Environmental'].mean()
    st.metric(" Avg ESG Environmental", f"{avg_esg:.1f}")
with col4:
    avg_water_intensity = filtered['WaterIntensity'].mean()
    st.metric(" Avg Water Intensity", f"{avg_water_intensity:.2f} m³/$M")

st.subheader("Customizable Scatter Plot")
x_axis = st.selectbox("X-axis", ['CarbonIntensity', 'WaterIntensity', 'EnergyIntensity', 'Revenue', 'ESG_Environmental', 'ESG_Social', 'ESG_Governance'], index=0)
y_axis = st.selectbox("Y-axis", ['ProfitMargin', 'ESG_Overall', 'MarketCap', 'GrowthRate'], index=0)
color_by = st.selectbox("Color by", ['Industry', 'Region', 'Year'], index=0)

fig_scatter = px.scatter(
    filtered,
    x=x_axis,
    y=y_axis,
    color=color_by,
    size='Revenue',
    hover_data=['CompanyName', 'Year', 'ProfitMargin', 'CarbonIntensity'],
    title=f"{y_axis} vs {x_axis}",
    labels={x_axis: x_axis.replace('_', ' '), y_axis: y_axis.replace('_', ' ')}
)
st.plotly_chart(fig_scatter, use_container_width=True)

st.subheader("Trends Over Time")
trend = filtered.groupby(['Year', 'Industry'])[['ProfitMargin', 'CarbonIntensity', 'ESG_Environmental']].mean().reset_index()

col_t1, col_t2, col_t3 = st.columns(3)
with col_t1:
    fig_margin = px.line(trend, x='Year', y='ProfitMargin', color='Industry', title="Profit Margin Trend")
    st.plotly_chart(fig_margin, use_container_width=True)
with col_t2:
    fig_carbon = px.line(trend, x='Year', y='CarbonIntensity', color='Industry', title="Carbon Intensity Trend")
    st.plotly_chart(fig_carbon, use_container_width=True)
with col_t3:
    fig_esg = px.line(trend, x='Year', y='ESG_Environmental', color='Industry', title="ESG Environmental Trend")
    st.plotly_chart(fig_esg, use_container_width=True)

st.subheader("Correlation Heatmap (Numerical Features)")
numeric_cols = ['ProfitMargin', 'CarbonIntensity', 'WaterIntensity', 'EnergyIntensity', 
                'ESG_Overall', 'ESG_Environmental', 'ESG_Social', 'ESG_Governance', 
                'Revenue', 'MarketCap', 'GrowthRate']
corr = filtered[numeric_cols].corr()
fig_corr = px.imshow(corr, text_auto=True, aspect="auto", color_continuous_scale='RdBu_r', title="Correlation Matrix")
st.plotly_chart(fig_corr, use_container_width=True)

st.subheader("Box Plots: Distribution by Industry")
col_box1, col_box2 = st.columns(2)
with col_box1:
    fig_box_margin = px.box(filtered, x='Industry', y='ProfitMargin', color='Industry', title="Profit Margin Distribution by Industry")
    st.plotly_chart(fig_box_margin, use_container_width=True)
with col_box2:
    fig_box_carbon = px.box(filtered, x='Industry', y='CarbonIntensity', color='Industry', title="Carbon Intensity Distribution by Industry")
    st.plotly_chart(fig_box_carbon, use_container_width=True)

st.subheader("Regional Analysis")
region_summary = filtered.groupby('Region').agg(
    avg_profit_margin=('ProfitMargin', 'mean'),
    avg_carbon_intensity=('CarbonIntensity', 'mean'),
    avg_esg=('ESG_Environmental', 'mean'),
    company_count=('CompanyID', 'nunique')
).reset_index()
fig_region = px.bar(region_summary, x='Region', y='avg_profit_margin', 
                    color='avg_carbon_intensity', 
                    title="Average Profit Margin by Region (colored by Carbon Intensity)",
                    labels={'avg_profit_margin': 'Avg Profit Margin (%)', 
                            'avg_carbon_intensity': 'Avg Carbon Intensity (tons/$M)'})
st.plotly_chart(fig_region, use_container_width=True)

st.subheader("Summary Statistics by Industry & Region")
summary = filtered.groupby(['Industry', 'Region']).agg(
    avg_profit_margin=('ProfitMargin', 'mean'),
    avg_carbon_intensity=('CarbonIntensity', 'mean'),
    avg_esg_env=('ESG_Environmental', 'mean'),
    count=('CompanyID', 'count')
).reset_index()
st.dataframe(summary, use_container_width=True)

st.subheader("Filtered Raw Data")
st.dataframe(filtered, use_container_width=True)

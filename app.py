import streamlit as st
import pandas as pd
import plotly.express as px
import plotly.graph_objects as go
from plotly.subplots import make_subplots
import requests
import json
import numpy as np
from datetime import datetime
import io
import base64
from PIL import Image
import folium
from streamlit_folium import st_folium
import geopandas as gpd
import matplotlib.pyplot as plt
import seaborn as sns

# Page configuration
st.set_page_config(
    page_title="World Bank Debt Analysis Dashboard",
    page_icon="📊",
    layout="wide",
    initial_sidebar_state="expanded"
)

# Custom CSS for better styling
st.markdown("""
<style>
    .main-header {
        font-size: 3rem;
        color: #1f77b4;
        text-align: center;
        margin-bottom: 2rem;
    }
    .metric-card {
        background-color: #f0f2f6;
        padding: 1rem;
        border-radius: 0.5rem;
        border-left: 4px solid #1f77b4;
    }
    .sidebar .sidebar-content {
        background-color: #f8f9fa;
    }
</style>
""", unsafe_allow_html=True)

# Title and description
st.markdown('<h1 class="main-header">World Bank Debt Analysis Dashboard</h1>', unsafe_allow_html=True)
st.markdown("""
<div style='text-align: center; margin-bottom: 2rem;'>
    <p style='font-size: 1.2rem; color: #666;'>
        Interactive analysis of PPG Bilateral Debt between India and South Asian countries
    </p>
</div>
""", unsafe_allow_html=True)

# Sidebar configuration
st.sidebar.title("Analysis Controls")

# Country mapping
COUNTRY_MAPPING = {
    'Bangladesh': 'BGD',
    'Bhutan': 'BTN', 
    'Sri Lanka': 'LKA',
    'Maldives': 'MDV',
    'Myanmar': 'MMR',
    'Nepal': 'NPL'
}

COUNTRY_CODES = {
    'BGD': 'Bangladesh',
    'BTN': 'Bhutan',
    'LKA': 'Sri Lanka', 
    'MDV': 'Maldives',
    'MMR': 'Myanmar',
    'NPL': 'Nepal'
}

# Function to load data from Excel files
@st.cache_data
def load_country_data(country_code):
    """Load data for a specific country from Excel file"""
    try:
        file_path = f"Bilateral Debt Data/{country_code}-646 PPG Bilateral Debt.xlsx"
        df = pd.read_excel(file_path)
        return df
    except Exception as e:
        st.error(f"Error loading data for {country_code}: {str(e)}")
        return None

# Function to load all data
@st.cache_data
def load_all_data():
    """Load all country data and combine into one dataframe"""
    all_data = []
    
    for country_name, country_code in COUNTRY_MAPPING.items():
        df = load_country_data(country_code)
        if df is not None:
            df['Country'] = country_name
            df['Country_Code'] = country_code
            all_data.append(df)
    
    if all_data:
        combined_df = pd.concat(all_data, ignore_index=True)
        # Clean and standardize column names
        combined_df.columns = [col.strip() for col in combined_df.columns]
        
        # Remove any unnamed columns
        combined_df = combined_df.loc[:, ~combined_df.columns.str.contains('^Unnamed')]
        
        return combined_df
    return None

# Load data
with st.spinner("Loading debt data..."):
    all_data = load_all_data()

if all_data is None:
    st.error("Failed to load data. Please check if the data files are available.")
    st.stop()

# Data preprocessing
def preprocess_data(df):
    """Clean and preprocess the data"""
    # Create a copy to avoid SettingWithCopyWarning
    df = df.copy()
    
    # Remove rows with missing values
    df = df.dropna()
    
    # Convert year to datetime if it's not already
    if 'year' in df.columns:
        df['year'] = pd.to_datetime(df['year'], format='%Y')
    
    # Convert debt amounts to numeric, removing any currency symbols
    if 'data' in df.columns:
        df['data'] = pd.to_numeric(df['data'], errors='coerce')
    
    # Calculate year-over-year growth percentage
    df = df.sort_values(['Country', 'year'])
    df['YoY Growth %'] = df.groupby('Country')['data'].pct_change() * 100
    
    return df

# Preprocess the data
all_data = preprocess_data(all_data)

# Sidebar controls
st.sidebar.markdown("### Analysis Settings")

# Country selection
selected_countries = st.sidebar.multiselect(
    "Select Countries to Analyze:",
    options=list(COUNTRY_MAPPING.keys()),
    default=list(COUNTRY_MAPPING.keys())[:3]  # Default to first 3 countries
)

# Time period selection
if 'year' in all_data.columns:
    min_year = all_data['year'].dt.year.min()
    max_year = all_data['year'].dt.year.max()
    
    year_range = st.sidebar.slider(
        "Select Year Range:",
        min_value=int(min_year),
        max_value=int(max_year),
        value=(int(min_year), int(max_year)),
        step=1
    )
else:
    year_range = (2000, 2020)

# Filter data based on selections
filtered_data = all_data[
    (all_data['Country'].isin(selected_countries)) &
    (all_data['year'].dt.year >= year_range[0]) &
    (all_data['year'].dt.year <= year_range[1])
]

# Main content area
if len(selected_countries) == 0:
    st.warning("Please select at least one country to analyze.")
else:
    # Key metrics row
    st.markdown("### Key Metrics")
    
    col1, col2, col3, col4 = st.columns(4)
    
    with col1:
        total_debt = filtered_data['data'].sum() / 1e9  # Convert to billions
        st.metric(
            label="Total Debt (Billions USD)",
            value=f"${total_debt:.2f}B",
            delta=f"{filtered_data['YoY Growth %'].mean():.1f}% avg growth"
        )
    
    with col2:
        avg_debt = filtered_data['data'].mean() / 1e6  # Convert to millions
        st.metric(
            label="Average Annual Debt (Millions USD)",
            value=f"${avg_debt:.1f}M"
        )
    
    with col3:
        max_debt_year = filtered_data.loc[filtered_data['data'].idxmax(), 'year'].year
        st.metric(
            label="Peak Debt Year",
            value=str(max_debt_year)
        )
    
    with col4:
        top_debtor = filtered_data.groupby('Country')['data'].sum().idxmax()
        st.metric(
            label="Top Debtor Country",
            value=top_debtor
        )

    # Tabs for different analysis views
    tab1, tab2, tab3, tab4, tab5 = st.tabs(["Trends Analysis", "Geographic View", "Comparative Analysis", "Detailed Insights", "Reports"])

    with tab1:
        st.markdown("### Debt Trends Over Time")
        
        # Line chart showing debt trends
        # Convert datetime to string for plotting to avoid warnings
        plot_data = filtered_data.copy()
        plot_data['year_str'] = plot_data['year'].dt.strftime('%Y')
        
        fig_trends = px.line(
            plot_data,
            x='year_str',
            y='data',
            color='Country',
            title='Debt Trends by Country Over Time',
            labels={'data': 'Debt Amount (USD)', 'year_str': 'Year'},
            hover_data=['YoY Growth %']
        )
        fig_trends.update_layout(height=500)
        st.plotly_chart(fig_trends, use_container_width=True)
        
        # Growth rate analysis
        st.markdown("### Year-over-Year Growth Analysis")
        
        col1, col2 = st.columns(2)
        
        with col1:
            # Growth rate chart
            fig_growth = px.bar(
                plot_data,
                x='year_str',
                y='YoY Growth %',
                color='Country',
                title='Year-over-Year Growth Rates',
                labels={'YoY Growth %': 'Growth Rate (%)'}
            )
            fig_growth.update_layout(height=400)
            st.plotly_chart(fig_growth, use_container_width=True)
        
        with col2:
            # Growth statistics
            growth_stats = filtered_data.groupby('Country')['YoY Growth %'].agg(['mean', 'std', 'min', 'max']).round(2)
            st.markdown("**Growth Statistics by Country:**")
            st.dataframe(growth_stats, use_container_width=True)

    with tab2:
        st.markdown("### Geographic Distribution of Debt")
        
        # Create a simple map visualization
        country_totals = filtered_data.groupby('Country')['data'].sum().reset_index()
        
        # Create a choropleth-like visualization using bar chart
        fig_map = px.bar(
            country_totals,
            x='Country',
            y='data',
            title='Total Debt by Country',
            color='data',
            color_continuous_scale='viridis',
            labels={'data': 'Total Debt (USD)'}
        )
        fig_map.update_layout(height=500)
        st.plotly_chart(fig_map, use_container_width=True)
        
        # Debt distribution pie chart
        st.markdown("### Debt Distribution")
        
        fig_pie = px.pie(
            country_totals,
            values='data',
            names='Country',
            title='Proportion of Total Debt by Country'
        )
        fig_pie.update_layout(height=400)
        st.plotly_chart(fig_pie, use_container_width=True)

    with tab3:
        st.markdown("### Side-by-Side Country Comparison")
        
        # Multi-line comparison
        fig_comparison = px.line(
            plot_data,
            x='year_str',
            y='data',
            color='Country',
            title='Country Comparison: Debt Over Time',
            labels={'data': 'Debt Amount (USD)'}
        )
        fig_comparison.update_layout(height=500)
        st.plotly_chart(fig_comparison, use_container_width=True)
        
        # Comparison table
        st.markdown("### Detailed Comparison Table")
        
        comparison_data = filtered_data.pivot_table(
            index='year',
            columns='Country',
            values='data',
            aggfunc='sum'
        ).fillna(0)
        
        # Convert index to string for display
        comparison_data.index = comparison_data.index.strftime('%Y')
        
        st.dataframe(comparison_data, use_container_width=True)
        
        # Statistical comparison
        st.markdown("### Statistical Summary")
        
        stats_summary = filtered_data.groupby('Country').agg({
            'data': ['sum', 'mean', 'std', 'min', 'max'],
            'YoY Growth %': ['mean', 'std']
        }).round(2)
        
        st.dataframe(stats_summary, use_container_width=True)

    with tab4:
        st.markdown("### Detailed Insights")
        
        col1, col2 = st.columns(2)
        
        with col1:
            # Top debt periods
            st.markdown("**Peak Debt Periods:**")
            peak_periods = filtered_data.nlargest(10, 'data')[['Country', 'year', 'data']].copy()
            peak_periods['year'] = peak_periods['year'].dt.strftime('%Y')
            st.dataframe(peak_periods, use_container_width=True)
        
        with col2:
            # Highest growth periods
            st.markdown("**Highest Growth Periods:**")
            growth_periods = filtered_data.nlargest(10, 'YoY Growth %')[['Country', 'year', 'YoY Growth %']].copy()
            growth_periods['year'] = growth_periods['year'].dt.strftime('%Y')
            st.dataframe(growth_periods, use_container_width=True)
        
        # Correlation analysis
        st.markdown("### Correlation Analysis")
        
        # Create correlation matrix for numerical columns
        numeric_data = filtered_data.select_dtypes(include=[np.number])
        if len(numeric_data.columns) > 1:
            correlation_matrix = numeric_data.corr()
            
            fig_corr = px.imshow(
                correlation_matrix,
                title='Correlation Matrix of Numerical Variables',
                color_continuous_scale='RdBu',
                aspect='auto'
            )
            fig_corr.update_layout(height=400)
            st.plotly_chart(fig_corr, use_container_width=True)

    with tab5:
        st.markdown("### Generate Reports")
        
        # Report generation options
        report_type = st.selectbox(
            "Select Report Type:",
            ["Executive Summary", "Detailed Analysis", "Country Comparison", "Custom Report"]
        )
        
        # Date range for report
        report_start = st.date_input("Report Start Date", value=datetime(year_range[0], 1, 1))
        report_end = st.date_input("Report End Date", value=datetime(year_range[1], 12, 31))
        
        # Generate report button
        if st.button("Generate Report"):
            with st.spinner("Generating report..."):
                # Create a simple report
                report_data = filtered_data.copy()
                
                # Generate report content
                report_content = f"""
# World Bank Debt Analysis Report
**Generated on:** {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}
**Analysis Period:** {report_start} to {report_end}
**Countries Analyzed:** {', '.join(selected_countries)}

## Executive Summary
- Total Debt Analyzed: ${total_debt:.2f} billion
- Average Annual Debt: ${avg_debt:.1f} million
- Number of Countries: {len(selected_countries)}
- Analysis Period: {year_range[1] - year_range[0] + 1} years

## Key Findings
- Top Debtor: {top_debtor}
- Peak Year: {max_debt_year}
- Average Growth Rate: {filtered_data['YoY Growth %'].mean():.2f}%

## Detailed Data
"""
                
                # Convert report to CSV for download
                csv = report_data.to_csv(index=False)
                
                # Create download buttons
                col1, col2 = st.columns(2)
                
                with col1:
                    st.download_button(
                        label="Download Data (CSV)",
                        data=csv,
                        file_name=f"debt_analysis_{datetime.now().strftime('%Y%m%d_%H%M%S')}.csv",
                        mime="text/csv"
                    )
                
                with col2:
                    st.download_button(
                        label="Download Report (TXT)",
                        data=report_content,
                        file_name=f"debt_report_{datetime.now().strftime('%Y%m%d_%H%M%S')}.txt",
                        mime="text/plain"
                    )
                
                # Display report preview
                st.markdown("### Report Preview")
                st.text_area("Report Content:", value=report_content, height=300)

# Footer
st.markdown("---")
st.markdown("""
<div style='text-align: center; color: #666;'>
    <p>World Bank Debt Analysis Dashboard | Data Source: World Bank API</p>
    <p>Built with Streamlit | Interactive analysis of PPG Bilateral Debt</p>
</div>
""", unsafe_allow_html=True) 
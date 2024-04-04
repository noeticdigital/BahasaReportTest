import streamlit as st
import pandas as pd
import plotly.express as px
import plotly.graph_objects as go
from assets.css import *

# Set Streamlit page configuration
st.set_page_config(
    page_title="Mellysa Salon Dashboard",
    page_icon="🧊",
    layout="wide",
    initial_sidebar_state="expanded",
)
st.markdown(main_style, unsafe_allow_html=True)
st.markdown(
    """
<style>
[data-testid="stMetricValue"] {
    font-size: 25px;
}
</style>
""",
    unsafe_allow_html=True,
)

# Define options for filters
all_month = ['January', 'February', 'March', 'April', 'May', 'June',
             'July', 'August', 'September', 'October', 'November', 'December']
quarter_months = {
    'Q1': ['January', 'February', 'March'],
    'Q2': ['April', 'May', 'June'],
    'Q3': ['July', 'August', 'September'],
    'Q4': ['October', 'November', 'December']
}

all_day = ['Monday', 'Tuesday', 'Wednesday', 'Thursday', 'Friday', 'Saturday', 'Sunday']

year_option = [2022, 2023]

current_year = 2023

def load_data(path: str):
    data = pd.read_csv(path)
    return data

df = load_data("./dataset/dataset_cleaned.csv")

def main_info(selected_months: list):
    month_filtered = df[df["Month"].isin(selected_months)]
    total_annual_revenue = month_filtered.groupby('Year')["Price"].sum().reset_index()
    total_annual_visits = month_filtered.groupby('Year')["Price"].count().reset_index()
    revenue_23 = int(total_annual_revenue[total_annual_revenue["Year"]==2023]["Price"].values[0])
    revenue_22 = int(total_annual_revenue[total_annual_revenue["Year"]==2022]["Price"].values[0])
    visits_23 = int(total_annual_visits[total_annual_visits["Year"]==2023]["Price"].values[0])
    visits_22 = int(total_annual_visits[total_annual_visits["Year"]==2022]["Price"].values[0])

    service_annual_revenue = month_filtered.groupby(['Service Name', 'Year'])["Price"].sum().reset_index()
    service_revenue_2023 = service_annual_revenue[service_annual_revenue['Year'] == 2023]
    service_revenue_2023_sorted = service_revenue_2023.sort_values(by='Price', ascending=False)
    highest_revenue_service_2023 = service_revenue_2023_sorted.iloc[0]['Service Name']
    service_revenue_2022 = service_annual_revenue[
        (service_annual_revenue['Year'] == 2022) &
        (service_annual_revenue['Service Name'] == highest_revenue_service_2023)
    ]
    service_popularity_annual = month_filtered.groupby(['Service Name', 'Year'])["Price"].count().reset_index()
    service_popularity_2023 = service_popularity_annual[service_popularity_annual['Year'] == 2023]
    service_popularity_2023_sorted = service_popularity_2023.sort_values(by='Price', ascending=False)
    most_popular_service_2023 = service_popularity_2023_sorted.iloc[0]['Service Name']
    service_popularity_2022 = service_popularity_annual[
        (service_popularity_annual['Year'] == 2022) &
        (service_popularity_annual['Service Name'] == most_popular_service_2023)
    ]

    revenue_service_23 = int(service_revenue_2023_sorted.iloc[0]['Price'])
    revenue_service_22 = int(service_revenue_2022.iloc[0]['Price'])
    visits_service_23 = int(service_popularity_2023_sorted.iloc[0]['Price'])
    visits_service_22 = int(service_popularity_2022.iloc[0]['Price'])
    st.subheader("Total 2023")
    st.metric("Revenue", f"{revenue_23:,} (IDR)", f"{(revenue_23-revenue_22):,} (IDR)")
    st.metric("Visits", f"{visits_23} (Visitors)", f"{visits_23-visits_22} (Visitors)")
    st.metric(f"Highest Revenue Service ({highest_revenue_service_2023})", f"{revenue_service_23:,} (IDR)", f"{(revenue_service_23-revenue_service_22):,} (IDR)")
    st.metric(f"Most Popular Service ({most_popular_service_2023})", f"{visits_service_23} (Visitors)", f"{visits_service_23-visits_service_22} (Visitors)")

# Further functions (daily_year_trend, plot_trend_year, service_top_rank, etc.) are similarly adjusted in terms of variable and text translations.


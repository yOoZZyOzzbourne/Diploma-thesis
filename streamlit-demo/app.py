import streamlit as st
import pandas as pd
import numpy as np
from datetime import datetime, timedelta
import plotly.express as px
import plotly.graph_objects as go

# Page config
st.set_page_config(
    page_title="Analytics Dashboard - Streamlit",
    layout="wide",
    initial_sidebar_state="expanded"
)

# Custom CSS for better styling
st.markdown("""
<style>
    .metric-card {
        background-color: #f0f2f6;
        padding: 20px;
        border-radius: 10px;
        border-left: 5px solid #1f77b4;
    }
    .stMetric {
        background-color: white;
        padding: 15px;
        border-radius: 8px;
        box-shadow: 0 2px 4px rgba(0,0,0,0.1);
    }
</style>
""", unsafe_allow_html=True)

# Initialize session state
if 'selected_region' not in st.session_state:
    st.session_state.selected_region = 'All'
if 'date_range' not in st.session_state:
    st.session_state.date_range = 30

# Generate realistic sales data
@st.cache_data
def generate_sales_data(days=90):
    np.random.seed(42)
    dates = pd.date_range(end=datetime.now(), periods=days, freq='D')
    regions = ['North America', 'Europe', 'Asia', 'South America']
    products = ['Product A', 'Product B', 'Product C', 'Product D', 'Product E']

    data = []
    for date in dates:
        for region in regions:
            for product in products:
                revenue = np.random.uniform(1000, 5000) * (1 + 0.1 * np.sin(date.dayofyear / 365 * 2 * np.pi))
                units = int(np.random.uniform(10, 100))
                data.append({
                    'Date': date,
                    'Region': region,
                    'Product': product,
                    'Revenue': revenue,
                    'Units': units,
                    'Customer_Count': int(np.random.uniform(5, 50))
                })

    return pd.DataFrame(data)

# Generate customer data
@st.cache_data
def generate_customer_data(n=100):
    np.random.seed(42)
    return pd.DataFrame({
        'Customer_ID': [f'CUST{i:04d}' for i in range(1, n+1)],
        'Name': [f'Customer {i}' for i in range(1, n+1)],
        'Total_Purchases': np.random.randint(1, 50, n),
        'Lifetime_Value': np.random.uniform(500, 50000, n),
        'Region': np.random.choice(['North America', 'Europe', 'Asia', 'South America'], n),
        'Status': np.random.choice(['Active', 'Inactive', 'VIP'], n, p=[0.6, 0.3, 0.1])
    })

df_sales = generate_sales_data()
df_customers = generate_customer_data()

# Sidebar
with st.sidebar:
    st.title("Dashboard Controls")

    # Date range filter
    date_range = st.slider(
        "Date Range (days)",
        min_value=7,
        max_value=90,
        value=30,
        key='date_filter'
    )

    # Region filter
    selected_region = st.selectbox(
        "Region",
        options=['All'] + list(df_sales['Region'].unique()),
        key='region_filter'
    )

    # Product filter
    selected_products = st.multiselect(
        "Products",
        options=df_sales['Product'].unique(),
        default=list(df_sales['Product'].unique())
    )

    st.markdown("---")

    # Export options
    st.subheader("Export Data")
    if st.button("Download CSV"):
        csv = df_sales.to_csv(index=False)
        st.download_button(
            label="Download Sales Data",
            data=csv,
            file_name=f"sales_data_{datetime.now().strftime('%Y%m%d')}.csv",
            mime="text/csv"
        )

# Filter data based on selections
df_filtered = df_sales[df_sales['Date'] >= (datetime.now() - timedelta(days=date_range))]
if selected_region != 'All':
    df_filtered = df_filtered[df_filtered['Region'] == selected_region]
if selected_products:
    df_filtered = df_filtered[df_filtered['Product'].isin(selected_products)]

# Main dashboard
st.title("Business Analytics Dashboard")
st.markdown("Real-time insights into sales performance and customer metrics")

# Top metrics
col1, col2, col3, col4 = st.columns(4)

total_revenue = df_filtered['Revenue'].sum()
total_units = df_filtered['Units'].sum()
avg_order_value = total_revenue / len(df_filtered) if len(df_filtered) > 0 else 0
customer_count = df_filtered['Customer_Count'].sum()

with col1:
    st.metric(
        "Total Revenue",
        f"${total_revenue:,.0f}",
        f"{np.random.uniform(-5, 15):.1f}%"
    )

with col2:
    st.metric(
        "Units Sold",
        f"{total_units:,}",
        f"{np.random.uniform(-3, 12):.1f}%"
    )

with col3:
    st.metric(
        "Avg Order Value",
        f"${avg_order_value:.0f}",
        f"{np.random.uniform(-2, 8):.1f}%"
    )

with col4:
    st.metric(
        "Total Customers",
        f"{customer_count:,}",
        f"{np.random.uniform(1, 20):.1f}%"
    )

st.markdown("---")

# Charts row 1
col1, col2 = st.columns(2)

with col1:
    st.subheader("Revenue Trend")
    revenue_by_date = df_filtered.groupby('Date')['Revenue'].sum().reset_index()
    fig_trend = px.line(
        revenue_by_date,
        x='Date',
        y='Revenue',
        title='Daily Revenue Trend'
    )
    fig_trend.update_layout(height=350)
    st.plotly_chart(fig_trend, use_container_width=True)

with col2:
    st.subheader("Revenue by Region")
    revenue_by_region = df_filtered.groupby('Region')['Revenue'].sum().reset_index()
    fig_region = px.pie(
        revenue_by_region,
        values='Revenue',
        names='Region',
        title='Revenue Distribution by Region'
    )
    fig_region.update_layout(height=350)
    st.plotly_chart(fig_region, use_container_width=True)

# Charts row 2
col1, col2 = st.columns(2)

with col1:
    st.subheader("Product Performance")
    product_perf = df_filtered.groupby('Product').agg({
        'Revenue': 'sum',
        'Units': 'sum'
    }).reset_index()

    fig_products = px.bar(
        product_perf,
        x='Product',
        y='Revenue',
        title='Revenue by Product',
        color='Units',
        color_continuous_scale='Blues'
    )
    fig_products.update_layout(height=350)
    st.plotly_chart(fig_products, use_container_width=True)

with col2:
    st.subheader("Sales Heatmap")
    df_filtered['Weekday'] = df_filtered['Date'].dt.day_name()
    df_filtered['Week'] = df_filtered['Date'].dt.isocalendar().week

    heatmap_data = df_filtered.groupby(['Week', 'Weekday'])['Revenue'].sum().reset_index()
    heatmap_pivot = heatmap_data.pivot(index='Weekday', columns='Week', values='Revenue')

    # Reorder weekdays
    weekday_order = ['Monday', 'Tuesday', 'Wednesday', 'Thursday', 'Friday', 'Saturday', 'Sunday']
    heatmap_pivot = heatmap_pivot.reindex(weekday_order)

    fig_heatmap = go.Figure(data=go.Heatmap(
        z=heatmap_pivot.values,
        x=heatmap_pivot.columns,
        y=heatmap_pivot.index,
        colorscale='YlOrRd'
    ))
    fig_heatmap.update_layout(
        title='Revenue Heatmap by Week and Day',
        height=350,
        xaxis_title='Week Number',
        yaxis_title='Day of Week'
    )
    st.plotly_chart(fig_heatmap, use_container_width=True)

st.markdown("---")

# Data tables section
tab1, tab2 = st.tabs(["Sales Data", "Customer Data"])

with tab1:
    st.subheader("Recent Sales Transactions")

    # Add search
    search_term = st.text_input("Search sales data", "")

    display_df = df_filtered.copy()
    if search_term:
        display_df = display_df[
            display_df.apply(lambda row: search_term.lower() in str(row.values).lower(), axis=1)
        ]

    # Format for display
    display_df['Revenue'] = display_df['Revenue'].apply(lambda x: f"${x:,.2f}")
    display_df['Date'] = display_df['Date'].dt.strftime('%Y-%m-%d')

    st.dataframe(
        display_df[['Date', 'Region', 'Product', 'Revenue', 'Units', 'Customer_Count']].tail(100),
        use_container_width=True,
        height=400
    )

with tab2:
    st.subheader("Customer Database")

    # Customer filters
    col1, col2 = st.columns(2)
    with col1:
        status_filter = st.multiselect(
            "Status",
            options=df_customers['Status'].unique(),
            default=list(df_customers['Status'].unique())
        )
    with col2:
        region_filter_cust = st.multiselect(
            "Region",
            options=df_customers['Region'].unique(),
            default=list(df_customers['Region'].unique())
        )

    filtered_customers = df_customers[
        (df_customers['Status'].isin(status_filter)) &
        (df_customers['Region'].isin(region_filter_cust))
    ]

    # Format for display
    display_customers = filtered_customers.copy()
    display_customers['Lifetime_Value'] = display_customers['Lifetime_Value'].apply(lambda x: f"${x:,.2f}")

    st.dataframe(
        display_customers,
        use_container_width=True,
        height=400
    )

    # Customer stats
    col1, col2, col3 = st.columns(3)
    with col1:
        st.metric("Total Customers", len(filtered_customers))
    with col2:
        avg_ltv = filtered_customers['Lifetime_Value'].str.replace('$', '').str.replace(',', '').astype(float).mean()
        st.metric("Avg Lifetime Value", f"${avg_ltv:,.0f}")
    with col3:
        vip_count = len(filtered_customers[filtered_customers['Status'] == 'VIP'])
        st.metric("VIP Customers", vip_count)

# Footer
st.markdown("---")
col1, col2, col3 = st.columns(3)
with col1:
    st.caption(f"Last updated: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
with col2:
    if st.button("Refresh Dashboard"):
        st.rerun()
with col3:
    st.caption(f"Showing data for last {date_range} days")

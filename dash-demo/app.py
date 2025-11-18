import dash
from dash import dcc, html, Input, Output, State, dash_table
import plotly.graph_objects as go
import plotly.express as px
import pandas as pd
import numpy as np
from datetime import datetime, timedelta

# Initialize the Dash app
app = dash.Dash(__name__, title="Analytics Dashboard - Dash", suppress_callback_exceptions=True)

# Generate sales data
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
                    'Status': np.random.choice(['Completed', 'Pending', 'Shipped'], p=[0.7, 0.2, 0.1])
                })

    return pd.DataFrame(data)

# Chart generators
def create_revenue_trend(df):
    revenue_by_date = df.groupby('Date')['Revenue'].sum().reset_index()
    fig = px.line(revenue_by_date, x='Date', y='Revenue', title='Revenue Trend')
    fig.update_traces(line_color='#1f77b4', line_width=3)
    fig.update_layout(
        height=350,
        margin=dict(l=40, r=40, t=40, b=40),
        plot_bgcolor='white',
        paper_bgcolor='#f8f9fa'
    )
    return fig

def create_product_chart(df):
    product_revenue = df.groupby('Product')['Revenue'].sum().reset_index()
    fig = px.bar(product_revenue, x='Product', y='Revenue', title='Revenue by Product')
    fig.update_traces(marker_color='#2ca02c')
    fig.update_layout(
        height=350,
        margin=dict(l=40, r=40, t=40, b=40),
        plot_bgcolor='white',
        paper_bgcolor='#f8f9fa'
    )
    return fig

def create_region_pie(df):
    region_revenue = df.groupby('Region')['Revenue'].sum().reset_index()
    fig = px.pie(region_revenue, values='Revenue', names='Region', title='Revenue by Region')
    fig.update_layout(
        height=350,
        margin=dict(l=40, r=40, t=40, b=40),
        paper_bgcolor='#f8f9fa'
    )
    return fig

def create_heatmap(df):
    df_copy = df.copy()
    df_copy['Weekday'] = pd.to_datetime(df_copy['Date']).dt.day_name()
    df_copy['Week'] = pd.to_datetime(df_copy['Date']).dt.isocalendar().week

    heatmap_data = df_copy.groupby(['Week', 'Weekday'])['Revenue'].sum().reset_index()
    heatmap_pivot = heatmap_data.pivot(index='Weekday', columns='Week', values='Revenue')

    weekday_order = ['Monday', 'Tuesday', 'Wednesday', 'Thursday', 'Friday', 'Saturday', 'Sunday']
    heatmap_pivot = heatmap_pivot.reindex(weekday_order)

    fig = go.Figure(data=go.Heatmap(
        z=heatmap_pivot.values,
        x=heatmap_pivot.columns,
        y=heatmap_pivot.index,
        colorscale='YlOrRd'
    ))
    fig.update_layout(
        title='Sales Heatmap',
        height=350,
        xaxis_title='Week',
        yaxis_title='Day',
        margin=dict(l=40, r=40, t=40, b=40),
        paper_bgcolor='#f8f9fa'
    )
    return fig

# Styles
CARD_STYLE = {
    'backgroundColor': 'white',
    'padding': '20px',
    'borderRadius': '10px',
    'boxShadow': '0 2px 4px rgba(0,0,0,0.1)',
    'marginBottom': '20px'
}

METRIC_STYLE = {
    'textAlign': 'center',
    'padding': '25px',
    'borderRadius': '10px',
    'color': 'white',
    'marginBottom': '15px'
}

# App layout
app.layout = html.Div([
    dcc.Location(id='url', refresh=False),
    dcc.Interval(id='interval-component', interval=30*1000, n_intervals=0),

    # Header
    html.Div([
        html.H1("Business Analytics Dashboard", style={'margin': '0', 'color': 'white'}),
        html.P("Real-time insights and data visualization", style={'margin': '5px 0 0 0', 'color': '#e0e0e0'})
    ], style={
        'backgroundColor': '#1f77b4',
        'padding': '30px',
        'marginBottom': '30px',
        'borderRadius': '0 0 15px 15px'
    }),

    # Navigation tabs
    html.Div([
        dcc.Tabs(id='tabs', value='dashboard', children=[
            dcc.Tab(label='Dashboard', value='dashboard'),
            dcc.Tab(label='Data Table', value='data-table'),
            dcc.Tab(label='Analytics', value='analytics'),
        ], style={'marginBottom': '20px'})
    ], style={'maxWidth': '1400px', 'margin': '0 auto', 'padding': '0 20px'}),

    # Main content
    html.Div(id='page-content', style={'maxWidth': '1400px', 'margin': '0 auto', 'padding': '0 20px'}),

], style={'fontFamily': 'Arial, sans-serif', 'backgroundColor': '#f5f5f5', 'minHeight': '100vh'})

# Dashboard tab layout
dashboard_layout = html.Div([
    # Filters
    html.Div([
        html.Div([
            html.Label("Date Range (days)", style={'fontWeight': 'bold', 'marginBottom': '5px'}),
            dcc.Slider(
                id='date-range-slider',
                min=7,
                max=90,
                step=1,
                value=30,
                marks={7: '7d', 30: '30d', 60: '60d', 90: '90d'},
                tooltip={"placement": "bottom", "always_visible": False}
            )
        ], style={'width': '30%', 'display': 'inline-block', 'padding': '10px'}),

        html.Div([
            html.Label("Region", style={'fontWeight': 'bold', 'marginBottom': '5px'}),
            dcc.Dropdown(
                id='region-dropdown',
                options=[{'label': r, 'value': r} for r in ['All', 'North America', 'Europe', 'Asia', 'South America']],
                value='All',
                clearable=False
            )
        ], style={'width': '30%', 'display': 'inline-block', 'padding': '10px'}),

        html.Div([
            html.Label("Products", style={'fontWeight': 'bold', 'marginBottom': '5px'}),
            dcc.Dropdown(
                id='product-dropdown',
                options=[{'label': p, 'value': p} for p in ['Product A', 'Product B', 'Product C', 'Product D', 'Product E']],
                value=['Product A', 'Product B', 'Product C', 'Product D', 'Product E'],
                multi=True,
                clearable=False
            )
        ], style={'width': '35%', 'display': 'inline-block', 'padding': '10px'}),
    ], style=CARD_STYLE),

    # Metrics row
    html.Div([
        html.Div([
            html.H4("Total Revenue", style={'margin': '0', 'fontSize': '16px'}),
            html.H2(id='metric-revenue', style={'margin': '10px 0 0 0'})
        ], style={**METRIC_STYLE, 'backgroundColor': '#1f77b4', 'width': '23%', 'display': 'inline-block', 'margin': '0 1%'}),

        html.Div([
            html.H4("Units Sold", style={'margin': '0', 'fontSize': '16px'}),
            html.H2(id='metric-units', style={'margin': '10px 0 0 0'})
        ], style={**METRIC_STYLE, 'backgroundColor': '#ff7f0e', 'width': '23%', 'display': 'inline-block', 'margin': '0 1%'}),

        html.Div([
            html.H4("Avg Order Value", style={'margin': '0', 'fontSize': '16px'}),
            html.H2(id='metric-avg', style={'margin': '10px 0 0 0'})
        ], style={**METRIC_STYLE, 'backgroundColor': '#2ca02c', 'width': '23%', 'display': 'inline-block', 'margin': '0 1%'}),

        html.Div([
            html.H4("Transactions", style={'margin': '0', 'fontSize': '16px'}),
            html.H2(id='metric-trans', style={'margin': '10px 0 0 0'})
        ], style={**METRIC_STYLE, 'backgroundColor': '#d62728', 'width': '23%', 'display': 'inline-block', 'margin': '0 1%'}),
    ], style={'marginBottom': '20px'}),

    # Charts row 1
    html.Div([
        html.Div([
            dcc.Graph(id='revenue-trend-chart')
        ], style={**CARD_STYLE, 'width': '48%', 'display': 'inline-block', 'marginRight': '2%'}),

        html.Div([
            dcc.Graph(id='region-pie-chart')
        ], style={**CARD_STYLE, 'width': '48%', 'display': 'inline-block'}),
    ]),

    # Charts row 2
    html.Div([
        html.Div([
            dcc.Graph(id='product-bar-chart')
        ], style={**CARD_STYLE, 'width': '48%', 'display': 'inline-block', 'marginRight': '2%'}),

        html.Div([
            dcc.Graph(id='heatmap-chart')
        ], style={**CARD_STYLE, 'width': '48%', 'display': 'inline-block'}),
    ]),
])

# Data table tab layout
data_table_layout = html.Div([
    html.Div([
        html.H2("Sales Transaction Data", style={'marginBottom': '20px'}),

        html.Div([
            html.Label("Search", style={'fontWeight': 'bold', 'marginBottom': '5px'}),
            dcc.Input(
                id='table-search',
                type='text',
                placeholder='Search data...',
                style={'width': '100%', 'padding': '10px', 'marginBottom': '15px', 'borderRadius': '5px', 'border': '1px solid #ddd'}
            )
        ]),

        dash_table.DataTable(
            id='sales-table',
            columns=[],
            data=[],
            style_table={'overflowX': 'auto'},
            style_cell={
                'textAlign': 'left',
                'padding': '12px',
                'fontFamily': 'Arial, sans-serif',
                'fontSize': '14px'
            },
            style_header={
                'backgroundColor': '#1f77b4',
                'color': 'white',
                'fontWeight': 'bold',
                'border': '1px solid #ddd'
            },
            style_data={
                'border': '1px solid #ddd',
                'backgroundColor': 'white'
            },
            style_data_conditional=[
                {
                    'if': {'row_index': 'odd'},
                    'backgroundColor': '#f9f9f9'
                }
            ],
            page_size=20,
            sort_action='native',
            filter_action='native'
        )
    ], style=CARD_STYLE)
])

# Analytics tab layout
analytics_layout = html.Div([
    html.Div([
        html.H2("Advanced Analytics", style={'marginBottom': '20px'}),

        html.Div([
            html.Div([
                html.H3("Key Performance Indicators", style={'color': '#1f77b4'}),
                html.Ul([
                    html.Li("Growth Rate: 12.5% MoM", style={'marginBottom': '10px'}),
                    html.Li("Customer Retention: 87%", style={'marginBottom': '10px'}),
                    html.Li("Average Deal Size: $3,245", style={'marginBottom': '10px'}),
                    html.Li("Conversion Rate: 24.3%", style={'marginBottom': '10px'}),
                ], style={'fontSize': '16px'}),

                html.H3("Top Performing Regions", style={'color': '#1f77b4', 'marginTop': '30px'}),
                html.Ol([
                    html.Li("North America - $2.4M", style={'marginBottom': '10px'}),
                    html.Li("Europe - $1.8M", style={'marginBottom': '10px'}),
                    html.Li("Asia - $1.5M", style={'marginBottom': '10px'}),
                    html.Li("South America - $0.9M", style={'marginBottom': '10px'}),
                ], style={'fontSize': '16px'}),
            ], style={'width': '48%', 'display': 'inline-block', 'verticalAlign': 'top', 'padding': '20px'}),

            html.Div([
                html.H3("Strategic Recommendations", style={'color': '#1f77b4'}),

                html.H4("Inventory Management", style={'marginTop': '20px', 'color': '#2ca02c'}),
                html.Ul([
                    html.Li("Increase stock for Product A by 20%"),
                    html.Li("Monitor Product E performance closely"),
                ], style={'marginBottom': '20px'}),

                html.H4("Marketing", style={'color': '#2ca02c'}),
                html.Ul([
                    html.Li("Focus campaigns on Asia-Pacific region"),
                    html.Li("Launch seasonal promotions in Q2"),
                    html.Li("Increase digital advertising spend by 15%"),
                ], style={'marginBottom': '20px'}),

                html.H4("Sales", style={'color': '#2ca02c'}),
                html.Ul([
                    html.Li("Prioritize high-value customer segments"),
                    html.Li("Improve conversion rates in South America"),
                    html.Li("Expand enterprise sales team"),
                ]),
            ], style={'width': '48%', 'display': 'inline-block', 'verticalAlign': 'top', 'padding': '20px', 'backgroundColor': '#f9f9f9', 'borderRadius': '10px'}),
        ]),
    ], style=CARD_STYLE)
])


# Callbacks
@app.callback(
    Output('page-content', 'children'),
    Input('tabs', 'value')
)
def render_content(tab):
    if tab == 'dashboard':
        return dashboard_layout
    elif tab == 'data-table':
        return data_table_layout
    elif tab == 'analytics':
        return analytics_layout

@app.callback(
    [Output('metric-revenue', 'children'),
     Output('metric-units', 'children'),
     Output('metric-avg', 'children'),
     Output('metric-trans', 'children'),
     Output('revenue-trend-chart', 'figure'),
     Output('region-pie-chart', 'figure'),
     Output('product-bar-chart', 'figure'),
     Output('heatmap-chart', 'figure')],
    [Input('date-range-slider', 'value'),
     Input('region-dropdown', 'value'),
     Input('product-dropdown', 'value'),
     Input('interval-component', 'n_intervals')]
)
def update_dashboard(date_range, region, products, n):
    df = generate_sales_data()

    # Filter by date
    cutoff_date = datetime.now() - timedelta(days=date_range)
    df_filtered = df[df['Date'] >= cutoff_date].copy()

    # Filter by region
    if region != 'All':
        df_filtered = df_filtered[df_filtered['Region'] == region]

    # Filter by products
    if products:
        df_filtered = df_filtered[df_filtered['Product'].isin(products)]

    # Calculate metrics
    total_revenue = df_filtered['Revenue'].sum()
    total_units = df_filtered['Units'].sum()
    avg_order = total_revenue / len(df_filtered) if len(df_filtered) > 0 else 0
    total_trans = len(df_filtered)

    # Format metrics
    revenue_str = f"${total_revenue:,.0f}"
    units_str = f"{total_units:,}"
    avg_str = f"${avg_order:.0f}"
    trans_str = f"{total_trans:,}"

    # Generate charts
    trend_chart = create_revenue_trend(df_filtered)
    pie_chart = create_region_pie(df_filtered)
    bar_chart = create_product_chart(df_filtered)
    heatmap = create_heatmap(df_filtered)

    return revenue_str, units_str, avg_str, trans_str, trend_chart, pie_chart, bar_chart, heatmap

@app.callback(
    [Output('sales-table', 'data'),
     Output('sales-table', 'columns')],
    [Input('date-range-slider', 'value'),
     Input('region-dropdown', 'value'),
     Input('product-dropdown', 'value'),
     Input('table-search', 'value')]
)
def update_table(date_range, region, products, search_value):
    df = generate_sales_data()

    # Filter by date
    cutoff_date = datetime.now() - timedelta(days=date_range)
    df_filtered = df[df['Date'] >= cutoff_date].copy()

    # Filter by region
    if region != 'All':
        df_filtered = df_filtered[df_filtered['Region'] == region]

    # Filter by products
    if products:
        df_filtered = df_filtered[df_filtered['Product'].isin(products)]

    # Format date and revenue
    df_filtered['Date'] = pd.to_datetime(df_filtered['Date']).dt.strftime('%Y-%m-%d')
    df_filtered['Revenue'] = df_filtered['Revenue'].apply(lambda x: f"${x:,.2f}")

    # Search filter
    if search_value:
        df_filtered = df_filtered[
            df_filtered.astype(str).apply(lambda x: x.str.contains(search_value, case=False, na=False)).any(axis=1)
        ]

    columns = [{"name": i, "id": i} for i in df_filtered.columns]
    data = df_filtered.to_dict('records')

    return data, columns


if __name__ == '__main__':
    print("Starting Dash Analytics Dashboard on http://localhost:8050")
    app.run(debug=True, host='0.0.0.0', port=8050)

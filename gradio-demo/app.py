import gradio as gr
import pandas as pd
import numpy as np
from datetime import datetime, timedelta
import plotly.express as px
import plotly.graph_objects as go

# Generate realistic data
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
                    'Date': date.strftime('%Y-%m-%d'),
                    'Region': region,
                    'Product': product,
                    'Revenue': revenue,
                    'Units': units,
                    'Status': np.random.choice(['Completed', 'Pending', 'Shipped'], p=[0.7, 0.2, 0.1])
                })

    return pd.DataFrame(data)

# Generate charts
def create_revenue_trend(df):
    df_chart = pd.DataFrame({'Date': pd.to_datetime(df['Date']), 'Revenue': df['Revenue']})
    revenue_by_date = df_chart.groupby('Date')['Revenue'].sum().reset_index()

    fig = px.line(revenue_by_date, x='Date', y='Revenue', title='Revenue Trend Over Time')
    fig.update_traces(line_color='#1f77b4', line_width=3)
    fig.update_layout(height=300)
    return fig

def create_product_chart(df):
    product_revenue = df.groupby('Product')['Revenue'].sum().reset_index()
    fig = px.bar(product_revenue, x='Product', y='Revenue', title='Revenue by Product',
                 color='Revenue', color_continuous_scale='Viridis')
    fig.update_layout(height=300)
    return fig

def create_region_pie(df):
    region_revenue = df.groupby('Region')['Revenue'].sum().reset_index()
    fig = px.pie(region_revenue, values='Revenue', names='Region', title='Revenue Distribution by Region')
    fig.update_layout(height=300)
    return fig

# Main dashboard update function
def update_dashboard(date_range, selected_region, selected_products):
    df = generate_sales_data()

    # Filter by date range
    cutoff_date = (datetime.now() - timedelta(days=date_range)).strftime('%Y-%m-%d')
    df_filtered = df[df['Date'] >= cutoff_date].copy()

    # Filter by region
    if selected_region != 'All':
        df_filtered = df_filtered[df_filtered['Region'] == selected_region]

    # Filter by products
    if selected_products:
        df_filtered = df_filtered[df_filtered['Product'].isin(selected_products)]

    # Calculate metrics
    total_revenue = df_filtered['Revenue'].sum()
    total_units = df_filtered['Units'].sum()
    avg_order = total_revenue / len(df_filtered) if len(df_filtered) > 0 else 0

    # Format metrics
    metrics_html = f"""
    <div style="display: grid; grid-template-columns: repeat(3, 1fr); gap: 15px; margin: 20px 0;">
        <div style="background: linear-gradient(135deg, #667eea 0%, #764ba2 100%); padding: 20px; border-radius: 10px; color: white; text-align: center;">
            <h3 style="margin: 0; font-size: 14px;">Total Revenue</h3>
            <p style="margin: 10px 0 0 0; font-size: 28px; font-weight: bold;">${total_revenue:,.0f}</p>
        </div>
        <div style="background: linear-gradient(135deg, #f093fb 0%, #f5576c 100%); padding: 20px; border-radius: 10px; color: white; text-align: center;">
            <h3 style="margin: 0; font-size: 14px;">Units Sold</h3>
            <p style="margin: 10px 0 0 0; font-size: 28px; font-weight: bold;">{total_units:,}</p>
        </div>
        <div style="background: linear-gradient(135deg, #4facfe 0%, #00f2fe 100%); padding: 20px; border-radius: 10px; color: white; text-align: center;">
            <h3 style="margin: 0; font-size: 14px;">Avg Order Value</h3>
            <p style="margin: 10px 0 0 0; font-size: 28px; font-weight: bold;">${avg_order:.0f}</p>
        </div>
    </div>
    """

    # Create charts
    trend_chart = create_revenue_trend(df_filtered)
    product_chart = create_product_chart(df_filtered)
    region_chart = create_region_pie(df_filtered)

    # Format dataframe for display
    display_df = df_filtered.copy()
    display_df['Revenue'] = display_df['Revenue'].apply(lambda x: f"${x:,.2f}")

    return metrics_html, trend_chart, product_chart, region_chart, display_df.head(50)

# Chat function for AI assistant
chat_history = []

def chat_response(message, history):
    responses = {
        "revenue": "Based on the current data, total revenue is performing well across all regions. North America leads with approximately 35% of total sales.",
        "trend": "The revenue trend shows seasonal patterns with peaks during mid-year. Consider focusing marketing efforts during Q2 and Q3.",
        "products": "Product A and Product C are the top performers. Product E might need additional marketing support.",
        "recommendation": "I recommend: 1) Increase inventory for Product A, 2) Launch targeted campaigns in Asia, 3) Optimize pricing for Product E.",
    }

    msg_lower = message.lower()
    response = "I can help you analyze the dashboard data. Try asking about revenue, trends, products, or recommendations."

    for key, value in responses.items():
        if key in msg_lower:
            response = value
            break

    return response

# File upload processor
def process_uploaded_file(file):
    if file is None:
        return "No file uploaded", None

    try:
        df = pd.read_csv(file.name)
        summary = f"""
        File processed successfully!

        Rows: {len(df)}
        Columns: {len(df.columns)}
        Column Names: {', '.join(df.columns.tolist())}

        Preview:
        """
        return summary, df.head(20)
    except Exception as e:
        return f"Error processing file: {str(e)}", None

# Create the Gradio interface
with gr.Blocks(title="Analytics Dashboard - Gradio", theme=gr.themes.Base()) as demo:
    gr.Markdown("# Business Analytics Dashboard")
    gr.Markdown("Interactive data visualization and AI-powered insights")

    with gr.Tab("Dashboard"):
        with gr.Row():
            with gr.Column(scale=1):
                gr.Markdown("### Filters")
                date_range = gr.Slider(
                    label="Date Range (days)",
                    minimum=7,
                    maximum=90,
                    value=30,
                    step=1
                )
                region_filter = gr.Dropdown(
                    label="Region",
                    choices=['All', 'North America', 'Europe', 'Asia', 'South America'],
                    value='All'
                )
                product_filter = gr.CheckboxGroup(
                    label="Products",
                    choices=['Product A', 'Product B', 'Product C', 'Product D', 'Product E'],
                    value=['Product A', 'Product B', 'Product C', 'Product D', 'Product E']
                )
                refresh_btn = gr.Button("Refresh Dashboard", variant="primary")

            with gr.Column(scale=3):
                metrics_display = gr.HTML()

                with gr.Row():
                    trend_plot = gr.Plot(label="Revenue Trend")
                    product_plot = gr.Plot(label="Product Performance")

                region_plot = gr.Plot(label="Regional Distribution")

                gr.Markdown("### Recent Transactions")
                data_table = gr.Dataframe(
                    headers=['Date', 'Region', 'Product', 'Revenue', 'Units', 'Status'],
                    interactive=False,
                    wrap=True
                )

        # Update dashboard on filter changes
        inputs = [date_range, region_filter, product_filter]
        outputs = [metrics_display, trend_plot, product_plot, region_plot, data_table]

        date_range.change(update_dashboard, inputs=inputs, outputs=outputs)
        region_filter.change(update_dashboard, inputs=inputs, outputs=outputs)
        product_filter.change(update_dashboard, inputs=inputs, outputs=outputs)
        refresh_btn.click(update_dashboard, inputs=inputs, outputs=outputs)

        # Initial load
        demo.load(update_dashboard, inputs=inputs, outputs=outputs)

    with gr.Tab("AI Assistant"):
        gr.Markdown("### Ask questions about your data")
        gr.Markdown("Try asking about: revenue, trends, products, or recommendations")

        chatbot = gr.Chatbot(height=400)
        msg = gr.Textbox(
            label="Your question",
            placeholder="What are the revenue trends?",
            lines=2
        )
        clear = gr.Button("Clear Chat")

        def respond(message, chat_history):
            bot_message = chat_response(message, chat_history)
            chat_history.append((message, bot_message))
            return "", chat_history

        msg.submit(respond, [msg, chatbot], [msg, chatbot])
        clear.click(lambda: None, None, chatbot, queue=False)

    with gr.Tab("Data Upload"):
        gr.Markdown("### Upload your own CSV data")
        gr.Markdown("Upload a CSV file to analyze custom data")

        with gr.Row():
            with gr.Column():
                file_input = gr.File(label="Upload CSV File", file_types=['.csv'])
                upload_btn = gr.Button("Process File", variant="primary")

            with gr.Column():
                upload_status = gr.Textbox(label="Status", lines=5, interactive=False)

        uploaded_data = gr.Dataframe(label="Data Preview", interactive=False)

        upload_btn.click(
            process_uploaded_file,
            inputs=[file_input],
            outputs=[upload_status, uploaded_data]
        )

    with gr.Tab("Analytics"):
        gr.Markdown("### Advanced Analytics")

        with gr.Row():
            with gr.Column():
                gr.Markdown("#### Key Performance Indicators")
                gr.Markdown("""
                - **Growth Rate:** 12.5% MoM
                - **Customer Retention:** 87%
                - **Average Deal Size:** $3,245
                - **Conversion Rate:** 24.3%
                """)

                gr.Markdown("#### Top Performing Regions")
                gr.Markdown("""
                1. North America - $2.4M
                2. Europe - $1.8M
                3. Asia - $1.5M
                4. South America - $0.9M
                """)

            with gr.Column():
                gr.Markdown("#### Recommendations")
                gr.Markdown("""
                **Inventory Management:**
                - Increase stock for Product A by 20%
                - Monitor Product E performance

                **Marketing:**
                - Focus campaigns on Asia-Pacific
                - Seasonal promotions in Q2

                **Sales:**
                - Prioritize high-value customers
                - Improve conversion in South America
                """)

if __name__ == "__main__":
    print("Starting Gradio Analytics Dashboard on http://localhost:7860")
    demo.launch(server_name="0.0.0.0", server_port=7860)

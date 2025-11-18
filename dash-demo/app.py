import dash
from dash import dcc, html, Input, Output, State
import plotly.graph_objects as go
import pandas as pd
import numpy as np
from datetime import datetime

# Initialize the Dash app
app = dash.Dash(__name__, title="IoT Dashboard - Dash")
app.config.suppress_callback_exceptions = True

# Generate mock temperature history
def generate_temp_history():
    times = pd.date_range(end=datetime.now(), periods=50, freq='1min')
    temps = 20 + np.cumsum(np.random.randn(50) * 0.5)

    fig = go.Figure()
    fig.add_trace(go.Scatter(
        x=times,
        y=temps,
        mode='lines',
        name='Temperature',
        line=dict(color='#ff7f0e', width=2)
    ))
    fig.update_layout(
        title='Temperature History',
        xaxis_title='Time',
        yaxis_title='Temperature (°C)',
        height=300,
        margin=dict(l=50, r=50, t=50, b=50),
        paper_bgcolor='#f8f9fa',
        plot_bgcolor='white'
    )
    return fig

# App layout
app.layout = html.Div([
    # Header
    html.H1("🏠 IoT Home Dashboard", style={'textAlign': 'center', 'color': '#2c3e50'}),
    html.Hr(),

    # Interval component for auto-refresh
    dcc.Interval(id='interval-component', interval=5*1000, n_intervals=0),

    # Main container
    html.Div([
        # Left column
        html.Div([
            # Light Controls
            html.H2("💡 Light Controls", style={'color': '#34495e'}),
            html.Div([
                html.Div([
                    html.Label("Living Room", style={'fontWeight': 'bold'}),
                    dcc.Checklist(
                        id='lr-light',
                        options=[{'label': ' Enable', 'value': 'on'}],
                        value=[],
                        style={'marginBottom': '10px'}
                    ),
                    html.Div(id='lr-status', style={'marginBottom': '20px'})
                ], style={'display': 'inline-block', 'width': '30%', 'padding': '10px'}),

                html.Div([
                    html.Label("Bedroom", style={'fontWeight': 'bold'}),
                    dcc.Checklist(
                        id='br-light',
                        options=[{'label': ' Enable', 'value': 'on'}],
                        value=[],
                        style={'marginBottom': '10px'}
                    ),
                    html.Div(id='br-status', style={'marginBottom': '20px'})
                ], style={'display': 'inline-block', 'width': '30%', 'padding': '10px'}),

                html.Div([
                    html.Label("Kitchen", style={'fontWeight': 'bold'}),
                    dcc.Checklist(
                        id='kt-light',
                        options=[{'label': ' Enable', 'value': 'on'}],
                        value=[],
                        style={'marginBottom': '10px'}
                    ),
                    html.Div(id='kt-status', style={'marginBottom': '20px'})
                ], style={'display': 'inline-block', 'width': '30%', 'padding': '10px'}),
            ]),

            html.Hr(),

            # Sensor Data
            html.H2("📊 Sensor Data", style={'color': '#34495e'}),
            html.Div([
                html.Div([
                    html.H3("🌡️ Temperature"),
                    html.Div(id='temp-display', style={'fontSize': '24px', 'fontWeight': 'bold'})
                ], style={'display': 'inline-block', 'width': '30%', 'padding': '10px',
                         'backgroundColor': '#e8f4f8', 'borderRadius': '10px', 'margin': '5px'}),

                html.Div([
                    html.H3("💧 Humidity"),
                    html.Div(id='humidity-display', style={'fontSize': '24px', 'fontWeight': 'bold'})
                ], style={'display': 'inline-block', 'width': '30%', 'padding': '10px',
                         'backgroundColor': '#e8f4f8', 'borderRadius': '10px', 'margin': '5px'}),

                html.Div([
                    html.H3("🚶 Motion"),
                    html.Div(id='motion-display', style={'fontSize': '24px', 'fontWeight': 'bold'})
                ], style={'display': 'inline-block', 'width': '30%', 'padding': '10px',
                         'backgroundColor': '#e8f4f8', 'borderRadius': '10px', 'margin': '5px'}),
            ], style={'marginBottom': '20px'}),

            # Temperature Chart
            dcc.Graph(id='temp-chart', figure=generate_temp_history()),

        ], style={'width': '65%', 'display': 'inline-block', 'verticalAlign': 'top', 'padding': '20px'}),

        # Right column
        html.Div([
            # Camera Feed
            html.H2("📹 Camera Feed", style={'color': '#34495e'}),
            dcc.Checklist(
                id='camera-toggle',
                options=[{'label': ' Enable Camera', 'value': 'on'}],
                value=['on'],
                style={'marginBottom': '10px'}
            ),
            html.Div(id='camera-status', style={'marginBottom': '10px'}),
            html.Div("📷 Mock Camera Feed",
                style={'backgroundColor': '#1f77b4', 'color': 'white',
                      'padding': '100px 20px', 'textAlign': 'center',
                      'borderRadius': '10px', 'fontSize': '24px',
                      'fontWeight': 'bold'}
            ),

            html.Hr(),

            # System Status
            html.H2("⚙️ System Status", style={'color': '#34495e'}),
            html.Div("✅ All systems operational",
                    style={'color': 'green', 'fontWeight': 'bold', 'marginBottom': '10px'}),
            html.Div(id='last-update', style={'marginBottom': '10px'}),

            html.H3("Connected Devices", style={'fontSize': '18px'}),
            html.Div(id='device-status'),

        ], style={'width': '30%', 'display': 'inline-block', 'verticalAlign': 'top',
                 'padding': '20px', 'backgroundColor': '#f8f9fa', 'borderRadius': '10px'}),

    ], style={'maxWidth': '1400px', 'margin': '0 auto'}),

], style={'fontFamily': 'Arial, sans-serif', 'padding': '20px'})


# Callbacks
@app.callback(
    Output('lr-status', 'children'),
    Input('lr-light', 'value')
)
def update_lr_status(value):
    if 'on' in value:
        return html.Span("ON", style={'color': 'green', 'fontWeight': 'bold'})
    return html.Span("OFF", style={'color': 'red', 'fontWeight': 'bold'})


@app.callback(
    Output('br-status', 'children'),
    Input('br-light', 'value')
)
def update_br_status(value):
    if 'on' in value:
        return html.Span("ON", style={'color': 'green', 'fontWeight': 'bold'})
    return html.Span("OFF", style={'color': 'red', 'fontWeight': 'bold'})


@app.callback(
    Output('kt-status', 'children'),
    Input('kt-light', 'value')
)
def update_kt_status(value):
    if 'on' in value:
        return html.Span("ON", style={'color': 'green', 'fontWeight': 'bold'})
    return html.Span("OFF", style={'color': 'red', 'fontWeight': 'bold'})


@app.callback(
    Output('camera-status', 'children'),
    Input('camera-toggle', 'value')
)
def update_camera_status(value):
    if 'on' in value:
        return html.Span("📷 Camera Active", style={'color': 'green', 'fontWeight': 'bold'})
    return html.Span("📷 Camera Disabled", style={'color': 'red', 'fontWeight': 'bold'})


@app.callback(
    [Output('temp-display', 'children'),
     Output('humidity-display', 'children'),
     Output('motion-display', 'children'),
     Output('temp-chart', 'figure'),
     Output('last-update', 'children'),
     Output('device-status', 'children')],
    [Input('interval-component', 'n_intervals'),
     Input('lr-light', 'value'),
     Input('br-light', 'value'),
     Input('kt-light', 'value'),
     Input('camera-toggle', 'value')]
)
def update_sensors(n, lr_light, br_light, kt_light, camera):
    # Generate mock sensor data
    temp = 20 + np.random.uniform(-2, 2)
    humidity = 45 + np.random.uniform(-5, 5)
    motion = "Detected" if np.random.random() < 0.2 else "Clear"

    # Update chart
    chart = generate_temp_history()

    # Last update time
    last_update = f"🕐 Last update: {datetime.now().strftime('%H:%M:%S')}"

    # Device status
    devices = [
        ("Living Room Light", 'on' in lr_light),
        ("Bedroom Light", 'on' in br_light),
        ("Kitchen Light", 'on' in kt_light),
        ("Camera", 'on' in camera),
        ("Temperature Sensor", True),
        ("Motion Detector", True),
    ]

    device_status = html.Div([
        html.Div(f"{'🟢' if status else '🔴'} {name}",
                style={'marginBottom': '5px'})
        for name, status in devices
    ])

    return f"{temp:.1f}°C", f"{humidity:.1f}%", motion, chart, last_update, device_status


if __name__ == '__main__':
    print("Starting Dash IoT Dashboard on http://localhost:8050")
    app.run(debug=True, host='0.0.0.0', port=8050)

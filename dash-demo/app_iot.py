"""IoT Control System - BroadbandLIGHT Demo"""
import dash
from dash import dcc, html, Input, Output, State, dash_table
import dash_daq as daq
import dash_bootstrap_components as dbc
import plotly.graph_objects as go
import plotly.express as px
import pandas as pd
import numpy as np
from datetime import datetime, timedelta
from mock_mqtt import mqtt_client
from database import log_sensor_reading, log_device_action, get_recent_sensor_data, get_device_logs

# Initialize app with Bootstrap theme
app = dash.Dash(__name__, external_stylesheets=[dbc.themes.BOOTSTRAP], suppress_callback_exceptions=True)
app.title = "BroadbandLIGHT IoT Control System"

# Styles
CARD_STYLE = {
    'boxShadow': '0 4px 6px rgba(0,0,0,0.1)',
    'borderRadius': '10px',
    'padding': '20px',
    'marginBottom': '20px',
    'backgroundColor': 'white'
}

# Layout
app.layout = dbc.Container([
    dcc.Interval(id='interval-sensors', interval=2000, n_intervals=0),
    dcc.Interval(id='interval-parking', interval=3000, n_intervals=0),
    dcc.Store(id='device-states'),

    # Header
    dbc.Row([
        dbc.Col([
            html.H1("BroadbandLIGHT IoT Control System", className='text-white mb-0'),
            html.P("Real-time monitoring and control", className='text-white-50 mb-0')
        ])
    ], className='bg-primary p-4 mb-4 rounded'),

    # Navigation
    dbc.Tabs([
        dbc.Tab(label='Dashboard', tab_id='dashboard'),
        dbc.Tab(label='Light Control', tab_id='lights'),
        dbc.Tab(label='Parking Lot', tab_id='parking'),
        dbc.Tab(label='Sensors', tab_id='sensors'),
        dbc.Tab(label='Cameras', tab_id='cameras'),
        dbc.Tab(label='Logs', tab_id='logs'),
    ], id='tabs', active_tab='dashboard'),

    html.Div(id='page-content', className='mt-4')

], fluid=True, style={'backgroundColor': '#f8f9fa', 'minHeight': '100vh', 'padding': '20px'})

# Dashboard Layout
def dashboard_layout():
    return dbc.Container([
        # Status Cards
        dbc.Row([
            dbc.Col([
                dbc.Card([
                    dbc.CardBody([
                        html.H4("System Status", className='text-primary'),
                        html.H2(id='system-status', children='ONLINE', className='text-success'),
                        html.P(id='mqtt-status', children='MQTT: Connected', className='mb-0')
                    ])
                ], style=CARD_STYLE)
            ], width=3),
            dbc.Col([
                dbc.Card([
                    dbc.CardBody([
                        html.H4("Active Lights", className='text-primary'),
                        html.H2(id='active-lights-count', children='0/3'),
                        html.P('Lights currently ON', className='mb-0')
                    ])
                ], style=CARD_STYLE)
            ], width=3),
            dbc.Col([
                dbc.Card([
                    dbc.CardBody([
                        html.H4("Parking Occupancy", className='text-primary'),
                        html.H2(id='parking-occupancy', children='0/6'),
                        html.P('Spots occupied', className='mb-0')
                    ])
                ], style=CARD_STYLE)
            ], width=3),
            dbc.Col([
                dbc.Card([
                    dbc.CardBody([
                        html.H4("Temperature", className='text-primary'),
                        html.H2(id='current-temp', children='--°C'),
                        html.P(id='temp-status', className='mb-0')
                    ])
                ], style=CARD_STYLE)
            ], width=3),
        ], className='mb-4'),

        # Real-time Sensor Charts
        dbc.Row([
            dbc.Col([
                dbc.Card([
                    dbc.CardBody([
                        html.H5('Temperature Trend', className='text-primary'),
                        dcc.Graph(id='temp-chart', config={'displayModeBar': False})
                    ])
                ], style=CARD_STYLE)
            ], width=6),
            dbc.Col([
                dbc.Card([
                    dbc.CardBody([
                        html.H5('Humidity & Light Level', className='text-primary'),
                        dcc.Graph(id='humidity-light-chart', config={'displayModeBar': False})
                    ])
                ], style=CARD_STYLE)
            ], width=6),
        ]),

        # Quick Controls
        dbc.Row([
            dbc.Col([
                dbc.Card([
                    dbc.CardBody([
                        html.H5('Quick Controls', className='text-primary mb-3'),
                        dbc.ButtonGroup([
                            dbc.Button('All Lights ON', id='btn-all-lights-on', color='success', className='me-2'),
                            dbc.Button('All Lights OFF', id='btn-all-lights-off', color='danger'),
                        ])
                    ])
                ], style=CARD_STYLE)
            ], width=12),
        ])
    ], fluid=True)

# Light Control Layout
def lights_layout():
    return dbc.Container([
        dbc.Row([
            # Light 1
            dbc.Col([
                dbc.Card([
                    dbc.CardBody([
                        html.H5('Light 1 - Main Entrance', className='text-primary mb-3'),

                        dbc.Row([
                            dbc.Col([
                                html.Label('Power', className='fw-bold'),
                                daq.PowerButton(
                                    id='light-1-power',
                                    on=False,
                                    color='#2ca02c',
                                    size=50
                                )
                            ], width=4),
                            dbc.Col([
                                daq.Indicator(
                                    id='light-1-indicator',
                                    value=False,
                                    color='#00FF00',
                                    label='Status',
                                    labelPosition='bottom'
                                )
                            ], width=4),
                        ], className='mb-3'),

                        html.Label('Brightness (%)', className='fw-bold'),
                        daq.Slider(
                            id='light-1-brightness',
                            min=0,
                            max=100,
                            value=50,
                            handleLabel={"showCurrentValue": True,"label": "%"},
                            marks={'0': '0%', '50': '50%', '100': '100%'},
                            color='#2ca02c'
                        ),

                        html.Label('Color Temperature (K)', className='fw-bold mt-3'),
                        daq.Slider(
                            id='light-1-color',
                            min=2700,
                            max=6500,
                            value=4000,
                            handleLabel={"showCurrentValue": True,"label": "K"},
                            marks={'2700': 'Warm', '4000': 'Neutral', '6500': 'Cool'},
                            color='#ff7f0e'
                        ),

                        html.Div(id='light-1-status', className='mt-3 p-2 bg-light rounded')
                    ])
                ], style=CARD_STYLE)
            ], width=4),

            # Light 2
            dbc.Col([
                dbc.Card([
                    dbc.CardBody([
                        html.H5('Light 2 - Parking Area', className='text-primary mb-3'),

                        dbc.Row([
                            dbc.Col([
                                html.Label('Power', className='fw-bold'),
                                daq.PowerButton(
                                    id='light-2-power',
                                    on=False,
                                    color='#2ca02c',
                                    size=50
                                )
                            ], width=4),
                            dbc.Col([
                                daq.Indicator(
                                    id='light-2-indicator',
                                    value=False,
                                    color='#00FF00',
                                    label='Status',
                                    labelPosition='bottom'
                                )
                            ], width=4),
                        ], className='mb-3'),

                        html.Label('Brightness (%)', className='fw-bold'),
                        daq.Slider(
                            id='light-2-brightness',
                            min=0,
                            max=100,
                            value=75,
                            handleLabel={"showCurrentValue": True,"label": "%"},
                            marks={'0': '0%', '50': '50%', '100': '100%'},
                            color='#2ca02c'
                        ),

                        html.Label('Color Temperature (K)', className='fw-bold mt-3'),
                        daq.Slider(
                            id='light-2-color',
                            min=2700,
                            max=6500,
                            value=3000,
                            handleLabel={"showCurrentValue": True,"label": "K"},
                            marks={'2700': 'Warm', '4000': 'Neutral', '6500': 'Cool'},
                            color='#ff7f0e'
                        ),

                        html.Div(id='light-2-status', className='mt-3 p-2 bg-light rounded')
                    ])
                ], style=CARD_STYLE)
            ], width=4),

            # Light 3
            dbc.Col([
                dbc.Card([
                    dbc.CardBody([
                        html.H5('Light 3 - Exit Area', className='text-primary mb-3'),

                        dbc.Row([
                            dbc.Col([
                                html.Label('Power', className='fw-bold'),
                                daq.PowerButton(
                                    id='light-3-power',
                                    on=False,
                                    color='#2ca02c',
                                    size=50
                                )
                            ], width=4),
                            dbc.Col([
                                daq.Indicator(
                                    id='light-3-indicator',
                                    value=False,
                                    color='#00FF00',
                                    label='Status',
                                    labelPosition='bottom'
                                )
                            ], width=4),
                        ], className='mb-3'),

                        html.Label('Brightness (%)', className='fw-bold'),
                        daq.Slider(
                            id='light-3-brightness',
                            min=0,
                            max=100,
                            value=100,
                            handleLabel={"showCurrentValue": True,"label": "%"},
                            marks={'0': '0%', '50': '50%', '100': '100%'},
                            color='#2ca02c'
                        ),

                        html.Label('Color Temperature (K)', className='fw-bold mt-3'),
                        daq.Slider(
                            id='light-3-color',
                            min=2700,
                            max=6500,
                            value=5000,
                            handleLabel={"showCurrentValue": True,"label": "K"},
                            marks={'2700': 'Warm', '4000': 'Neutral', '6500': 'Cool'},
                            color='#ff7f0e'
                        ),

                        html.Div(id='light-3-status', className='mt-3 p-2 bg-light rounded')
                    ])
                ], style=CARD_STYLE)
            ], width=4),
        ])
    ], fluid=True)

# Parking Layout
def parking_layout():
    return dbc.Container([
        dbc.Row([
            dbc.Col([
                dbc.Card([
                    dbc.CardBody([
                        html.H5('Parking Lot Overview', className='text-primary mb-3'),
                        dcc.Graph(id='parking-map', config={'displayModeBar': False})
                    ])
                ], style=CARD_STYLE)
            ], width=8),
            dbc.Col([
                dbc.Card([
                    dbc.CardBody([
                        html.H5('Parking Statistics', className='text-primary mb-3'),
                        html.Div(id='parking-stats')
                    ])
                ], style=CARD_STYLE)
            ], width=4),
        ])
    ], fluid=True)

# Sensors Layout
def sensors_layout():
    return dbc.Container([
        dbc.Row([
            dbc.Col([
                dbc.Card([
                    dbc.CardBody([
                        html.H5('Live Sensor Readings', className='text-primary mb-4'),
                        dbc.Row([
                            dbc.Col([
                                daq.Gauge(
                                    id='gauge-temp',
                                    label='Temperature (°C)',
                                    min=0,
                                    max=50,
                                    value=20,
                                    showCurrentValue=True,
                                    color={"gradient":True,"ranges":{"blue":[0,15],"green":[15,25],"yellow":[25,35],"red":[35,50]}}
                                )
                            ], width=3),
                            dbc.Col([
                                daq.Gauge(
                                    id='gauge-humidity',
                                    label='Humidity (%)',
                                    min=0,
                                    max=100,
                                    value=45,
                                    showCurrentValue=True,
                                    color={"gradient":True,"ranges":{"red":[0,30],"yellow":[30,40],"green":[40,60],"yellow":[60,70],"red":[70,100]}}
                                )
                            ], width=3),
                            dbc.Col([
                                daq.Gauge(
                                    id='gauge-light',
                                    label='Light Level (lux)',
                                    min=0,
                                    max=1000,
                                    value=500,
                                    showCurrentValue=True,
                                    color={"gradient":True,"ranges":{"blue":[0,200],"green":[200,600],"yellow":[600,1000]}}
                                )
                            ], width=3),
                            dbc.Col([
                                daq.Indicator(
                                    id='motion-indicator',
                                    label='Motion Detected',
                                    value=False,
                                    color='#FF5E5E',
                                    size=50,
                                    labelPosition='bottom'
                                )
                            ], width=3),
                        ])
                    ])
                ], style=CARD_STYLE)
            ], width=12),
        ]),

        dbc.Row([
            dbc.Col([
                dbc.Card([
                    dbc.CardBody([
                        html.H5('Sensor History', className='text-primary'),
                        dcc.Graph(id='sensor-history-chart')
                    ])
                ], style=CARD_STYLE)
            ], width=12),
        ])
    ], fluid=True)

# Cameras Layout
def cameras_layout():
    return dbc.Container([
        dbc.Row([
            dbc.Col([
                dbc.Card([
                    dbc.CardBody([
                        html.H5('Camera 1 - Entrance', className='text-primary mb-3'),
                        daq.BooleanSwitch(
                            id='camera-1-switch',
                            on=True,
                            label='Camera Active',
                            labelPosition='top'
                        ),
                        daq.BooleanSwitch(
                            id='camera-1-recording',
                            on=False,
                            label='Recording',
                            labelPosition='top',
                            color='#FF5E5E',
                            className='mt-3'
                        ),
                        html.Div([
                            html.Div('Live Feed Placeholder',
                                style={
                                    'backgroundColor': '#1f77b4',
                                    'color': 'white',
                                    'padding': '100px',
                                    'textAlign': 'center',
                                    'borderRadius': '10px',
                                    'marginTop': '20px'
                                })
                        ])
                    ])
                ], style=CARD_STYLE)
            ], width=6),
            dbc.Col([
                dbc.Card([
                    dbc.CardBody([
                        html.H5('Camera 2 - Parking Lot', className='text-primary mb-3'),
                        daq.BooleanSwitch(
                            id='camera-2-switch',
                            on=True,
                            label='Camera Active',
                            labelPosition='top'
                        ),
                        daq.BooleanSwitch(
                            id='camera-2-recording',
                            on=False,
                            label='Recording',
                            labelPosition='top',
                            color='#FF5E5E',
                            className='mt-3'
                        ),
                        html.Div([
                            html.Div('Live Feed Placeholder',
                                style={
                                    'backgroundColor': '#2ca02c',
                                    'color': 'white',
                                    'padding': '100px',
                                    'textAlign': 'center',
                                    'borderRadius': '10px',
                                    'marginTop': '20px'
                                })
                        ])
                    ])
                ], style=CARD_STYLE)
            ], width=6),
        ])
    ], fluid=True)

# Logs Layout
def logs_layout():
    return dbc.Container([
        dbc.Row([
            dbc.Col([
                dbc.Card([
                    dbc.CardBody([
                        html.H5('Device Control Logs', className='text-primary mb-3'),
                        html.Div(id='device-logs-table')
                    ])
                ], style=CARD_STYLE)
            ], width=12),
        ])
    ], fluid=True)

# Callbacks
@app.callback(
    Output('page-content', 'children'),
    Input('tabs', 'active_tab')
)
def render_tab(active_tab):
    if active_tab == 'dashboard':
        return dashboard_layout()
    elif active_tab == 'lights':
        return lights_layout()
    elif active_tab == 'parking':
        return parking_layout()
    elif active_tab == 'sensors':
        return sensors_layout()
    elif active_tab == 'cameras':
        return cameras_layout()
    elif active_tab == 'logs':
        return logs_layout()

# Light controls - Light 1
@app.callback(
    [Output('light-1-indicator', 'value'),
     Output('light-1-status', 'children')],
    [Input('light-1-power', 'on'),
     Input('light-1-brightness', 'value'),
     Input('light-1-color', 'value')]
)
def control_light_1(power, brightness, color_temp):
    mqtt_client.publish('lights/light_1/status', 'on' if power else 'off')
    mqtt_client.publish('lights/light_1/brightness', str(brightness))
    mqtt_client.publish('lights/light_1/color_temp', str(color_temp))

    log_device_action('light_1', 'light', 'power', power)
    log_device_action('light_1', 'light', 'brightness', brightness)

    status = f"Power: {'ON' if power else 'OFF'} | Brightness: {brightness}% | Color: {color_temp}K"
    return power, status

# Light 2 controls
@app.callback(
    [Output('light-2-indicator', 'value'),
     Output('light-2-status', 'children')],
    [Input('light-2-power', 'on'),
     Input('light-2-brightness', 'value'),
     Input('light-2-color', 'value')]
)
def control_light_2(power, brightness, color_temp):
    mqtt_client.publish('lights/light_2/status', 'on' if power else 'off')
    mqtt_client.publish('lights/light_2/brightness', str(brightness))
    mqtt_client.publish('lights/light_2/color_temp', str(color_temp))

    log_device_action('light_2', 'light', 'power', power)

    status = f"Power: {'ON' if power else 'OFF'} | Brightness: {brightness}% | Color: {color_temp}K"
    return power, status

# Light 3 controls
@app.callback(
    [Output('light-3-indicator', 'value'),
     Output('light-3-status', 'children')],
    [Input('light-3-power', 'on'),
     Input('light-3-brightness', 'value'),
     Input('light-3-color', 'value')]
)
def control_light_3(power, brightness, color_temp):
    mqtt_client.publish('lights/light_3/status', 'on' if power else 'off')
    mqtt_client.publish('lights/light_3/brightness', str(brightness))
    mqtt_client.publish('lights/light_3/color_temp', str(color_temp))

    log_device_action('light_3', 'light', 'power', power)

    status = f"Power: {'ON' if power else 'OFF'} | Brightness: {brightness}% | Color: {color_temp}K"
    return power, status

# Dashboard updates
@app.callback(
    [Output('active-lights-count', 'children'),
     Output('parking-occupancy', 'children'),
     Output('current-temp', 'children'),
     Output('temp-status', 'children'),
     Output('temp-chart', 'figure'),
     Output('humidity-light-chart', 'figure')],
    Input('interval-sensors', 'n_intervals')
)
def update_dashboard(n):
    # Count active lights
    lights_on = sum(1 for light_id in ['light_1', 'light_2', 'light_3']
                    if mqtt_client.get_device_state(light_id).get('status', False))

    # Count occupied parking
    parking_occupied = sum(1 for i in range(1, 7)
                          if mqtt_client.get_device_state(f'parking_{i}').get('occupied', False))

    # Get sensor data
    sensor_data = mqtt_client.get_sensor_data()
    temp = sensor_data['temperature']

    # Log sensor reading
    log_sensor_reading('sensor_1', 'temperature', temp, '°C')
    log_sensor_reading('sensor_1', 'humidity', sensor_data['humidity'], '%')

    temp_status = 'Normal' if 15 <= temp <= 25 else 'Alert'

    # Generate charts
    times = pd.date_range(end=datetime.now(), periods=30, freq='1min')
    temps = 20 + np.cumsum(np.random.randn(30) * 0.3)

    temp_fig = go.Figure()
    temp_fig.add_trace(go.Scatter(x=times, y=temps, mode='lines', fill='tozeroy',
                                  line=dict(color='#1f77b4', width=2)))
    temp_fig.update_layout(height=250, margin=dict(l=40, r=20, t=20, b=40),
                          xaxis_title='Time', yaxis_title='°C',
                          plot_bgcolor='white')

    humidity_light_fig = go.Figure()
    humidity_light_fig.add_trace(go.Scatter(x=times, y=45 + np.cumsum(np.random.randn(30) * 1),
                                           name='Humidity (%)', line=dict(color='#2ca02c')))
    humidity_light_fig.add_trace(go.Scatter(x=times, y=500 + np.cumsum(np.random.randn(30) * 20),
                                           name='Light (lux)', yaxis='y2', line=dict(color='#ff7f0e')))
    humidity_light_fig.update_layout(
        height=250, margin=dict(l=40, r=40, t=20, b=40),
        xaxis_title='Time',
        yaxis=dict(title='Humidity (%)'),
        yaxis2=dict(title='Light (lux)', overlaying='y', side='right'),
        plot_bgcolor='white'
    )

    return (f'{lights_on}/3', f'{parking_occupied}/6', f"{temp:.1f}°C",
            temp_status, temp_fig, humidity_light_fig)

# Sensor gauges update
@app.callback(
    [Output('gauge-temp', 'value'),
     Output('gauge-humidity', 'value'),
     Output('gauge-light', 'value'),
     Output('motion-indicator', 'value'),
     Output('sensor-history-chart', 'figure')],
    Input('interval-sensors', 'n_intervals')
)
def update_sensors(n):
    sensor_data = mqtt_client.get_sensor_data()

    # History chart
    times = pd.date_range(end=datetime.now(), periods=50, freq='30s')
    temp_history = 20 + np.cumsum(np.random.randn(50) * 0.3)
    humidity_history = 45 + np.cumsum(np.random.randn(50) * 1)

    fig = go.Figure()
    fig.add_trace(go.Scatter(x=times, y=temp_history, name='Temperature (°C)',
                            line=dict(color='#1f77b4', width=2)))
    fig.add_trace(go.Scatter(x=times, y=humidity_history, name='Humidity (%)',
                            line=dict(color='#2ca02c', width=2), yaxis='y2'))
    fig.update_layout(
        height=350,
        xaxis_title='Time',
        yaxis=dict(title='Temperature (°C)'),
        yaxis2=dict(title='Humidity (%)', overlaying='y', side='right'),
        plot_bgcolor='white',
        margin=dict(l=40, r=40, t=20, b=40)
    )

    return (sensor_data['temperature'], sensor_data['humidity'],
            sensor_data['light_level'], sensor_data['motion_detected'], fig)

# Parking map
@app.callback(
    [Output('parking-map', 'figure'),
     Output('parking-stats', 'children')],
    Input('interval-parking', 'n_intervals')
)
def update_parking(n):
    # Create parking lot visualization
    spots = []
    for i in range(1, 7):
        spot_data = mqtt_client.get_device_state(f'parking_{i}')
        occupied = spot_data.get('occupied', False)
        duration = spot_data.get('duration', 0)
        spots.append({
            'id': f'P{i}',
            'x': (i-1) % 3,
            'y': (i-1) // 3,
            'occupied': occupied,
            'duration': duration
        })

    df = pd.DataFrame(spots)

    fig = go.Figure()

    # Draw parking spots
    for _, spot in df.iterrows():
        color = '#d62728' if spot['occupied'] else '#2ca02c'
        fig.add_trace(go.Scatter(
            x=[spot['x']],
            y=[spot['y']],
            mode='markers+text',
            marker=dict(size=100, color=color, symbol='square'),
            text=spot['id'],
            textposition='middle center',
            textfont=dict(size=20, color='white'),
            name=spot['id'],
            hovertemplate=f"<b>{spot['id']}</b><br>Status: {'Occupied' if spot['occupied'] else 'Free'}<br>Duration: {spot['duration']} min"
        ))

    fig.update_layout(
        height=400,
        showlegend=False,
        xaxis=dict(showgrid=False, showticklabels=False, range=[-0.5, 2.5]),
        yaxis=dict(showgrid=False, showticklabels=False, range=[-0.5, 1.5]),
        plot_bgcolor='#f8f9fa',
        margin=dict(l=20, r=20, t=20, b=20)
    )

    # Statistics
    occupied_count = df['occupied'].sum()
    total_spots = len(df)
    occupancy_rate = (occupied_count / total_spots) * 100
    avg_duration = df[df['occupied']]['duration'].mean() if occupied_count > 0 else 0

    stats = html.Div([
        html.P([html.Strong('Total Spots: '), f'{total_spots}']),
        html.P([html.Strong('Occupied: '), f'{occupied_count}']),
        html.P([html.Strong('Available: '), f'{total_spots - occupied_count}']),
        html.P([html.Strong('Occupancy Rate: '), f'{occupancy_rate:.1f}%']),
        html.P([html.Strong('Avg Duration: '), f'{avg_duration:.0f} min']),
    ])

    return fig, stats

# Device logs
@app.callback(
    Output('device-logs-table', 'children'),
    Input('interval-sensors', 'n_intervals')
)
def update_logs(n):
    logs = get_device_logs(limit=20)

    if not logs:
        return html.P('No logs available')

    df = pd.DataFrame([{
        'Timestamp': log.timestamp.strftime('%Y-%m-%d %H:%M:%S'),
        'Device': log.device_id,
        'Type': log.device_type,
        'Action': log.action,
        'Value': log.value
    } for log in logs])

    return dash_table.DataTable(
        data=df.to_dict('records'),
        columns=[{'name': i, 'id': i} for i in df.columns],
        style_cell={'textAlign': 'left', 'padding': '10px'},
        style_header={'backgroundColor': '#1f77b4', 'color': 'white', 'fontWeight': 'bold'},
        style_data_conditional=[
            {'if': {'row_index': 'odd'}, 'backgroundColor': '#f8f9fa'}
        ],
        page_size=10
    )

if __name__ == '__main__':
    print("Starting BroadbandLIGHT IoT Control System on http://localhost:8050")
    app.run(debug=True, host='0.0.0.0', port=8050)

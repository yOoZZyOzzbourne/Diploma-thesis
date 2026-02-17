"""
Parking Lot Control System - Dash Application
BroadbandLIGHT Smart Parking @ VŠB-TUO
"""
import dash
from dash import html, dcc, Input, Output, State, ALL, MATCH, callback_context
import dash_bootstrap_components as dbc
import dash_daq as daq
import plotly.graph_objects as go
from datetime import datetime
import sys
import os
import requests
from requests.auth import HTTPBasicAuth, HTTPDigestAuth
import base64
from flask import Response

# Add parent directory to path for imports
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from config.devices import LIGHTS, BEACONS, CAMERAS, WEATHER_STATION
from src.mqtt_client import ParkingLotMQTT
from src.weather_client import WeatherStationClient

# Initialize Dash app
app = dash.Dash(
    __name__,
    external_stylesheets=[dbc.themes.DARKLY, dbc.icons.FONT_AWESOME],
    suppress_callback_exceptions=True
)
app.title = "Smart Parking Control"

# Get Flask server for adding routes
server = app.server

# Initialize MQTT client
mqtt_client = ParkingLotMQTT()

# Initialize Weather Station client
weather_client = WeatherStationClient(
    host=WEATHER_STATION['ip'],
    port=WEATHER_STATION['port']
)


# ============= FLASK ROUTES =============

@server.route('/camera/<int:cam_id>/snapshot')
def camera_snapshot(cam_id):
    """Proxy camera snapshot with authentication"""
    if cam_id not in CAMERAS:
        print(f"Camera {cam_id} not found")
        return "Camera not found", 404

    cam_data = CAMERAS[cam_id]

    # Check if camera is configured
    if not cam_data.get('snapshot_url'):
        print(f"Camera {cam_id} not configured")
        return "Camera not configured", 404

    try:
        snapshot_url = cam_data['snapshot_url']
        username = cam_data['username']
        print(f"Fetching camera {cam_id} from: {snapshot_url}")

        # Fetch image from camera with authentication
        # Use Digest auth for AXIS cameras, Basic for DAHUA
        auth_method = HTTPDigestAuth if cam_data['type'] == 'axis' else HTTPBasicAuth
        response = requests.get(
            snapshot_url,
            auth=auth_method(username, cam_data['password']),
            timeout=5,
            verify=False  # Disable SSL verification for local cameras
        )

        print(f"Camera {cam_id} response status: {response.status_code}")

        if response.status_code == 200:
            return Response(response.content, mimetype='image/jpeg')
        else:
            error_msg = f"Camera error: {response.status_code} - {response.text[:200]}"
            print(error_msg)
            return error_msg, 500

    except Exception as e:
        error_msg = f"Error fetching camera {cam_id}: {str(e)}"
        print(error_msg)
        return error_msg, 500

# ============= LAYOUT COMPONENTS =============

def create_navbar():
    """Create navigation bar"""
    return dbc.Navbar(
        dbc.Container([
            dbc.Row([
                dbc.Col(html.I(className="fas fa-parking fa-2x text-light"), width="auto"),
                dbc.Col(dbc.NavbarBrand("Smart Parking Control System", className="ms-2")),
            ], align="center"),
            dbc.Row([
                dbc.Col([
                    html.Div([
                        daq.Indicator(
                            id='mqtt-status',
                            value=False,
                            color="#00EA64",
                            size=20,
                            className="d-inline-block"
                        ),
                        html.Span("MQTT", className="ms-2 text-light")
                    ], className="d-inline-flex align-items-center")
                ], width="auto")
            ], align="center")
        ], fluid=True),
        color="dark",
        dark=True,
        className="mb-4"
    )


def create_light_control_card(pole_id: int, pole_data: dict):
    """Create control card for a single light pole"""
    devices = pole_data['devices']

    controls = []
    for idx, device in enumerate(devices):
        controls.append(
            dbc.Card([
                dbc.CardHeader([
                    html.I(className="fas fa-lightbulb me-2"),
                    f"{device['type']}"
                ]),
                dbc.CardBody([
                    html.Label("Výkon (%)"),
                    daq.Slider(
                        id={'type': 'light-slider', 'pole': pole_id, 'device': idx},
                        min=0,
                        max=100,
                        value=0,
                        handleLabel={"showCurrentValue": True, "label": "%"},
                        step=1,
                        size=200
                    ),
                    html.Div([
                        dbc.Button(
                            "Vypnout",
                            id={'type': 'light-off-btn', 'pole': pole_id, 'device': idx},
                            color="danger",
                            size="sm",
                            className="me-2"
                        ),
                        dbc.Button(
                            "50%",
                            id={'type': 'light-50-btn', 'pole': pole_id, 'device': idx},
                            color="warning",
                            size="sm",
                            className="me-2"
                        ),
                        dbc.Button(
                            "100%",
                            id={'type': 'light-100-btn', 'pole': pole_id, 'device': idx},
                            color="success",
                            size="sm"
                        ),
                    ], className="mt-2"),
                    html.Small(f"MAC: {device['mac']}", className="text-muted mt-2 d-block")
                ])
            ], className="mb-2")
        )

    return dbc.Card([
        dbc.CardHeader([
            html.H5([
                html.I(className="fas fa-traffic-light me-2"),
                pole_data['name']
            ], className="mb-0")
        ]),
        dbc.CardBody(controls)
    ], className="mb-3")


def create_beacon_control():
    """Create beacon control panel"""
    beacon_cards = []
    for beacon_id, beacon_data in BEACONS.items():
        beacon_cards.append(
            dbc.Col([
                dbc.Card([
                    dbc.CardHeader([
                        html.I(className="fas fa-exclamation-triangle me-2"),
                        beacon_data['name']
                    ]),
                    dbc.CardBody([
                        daq.BooleanSwitch(
                            id={'type': 'beacon-switch', 'id': beacon_id},
                            on=False,
                            color="#FF5E5E",
                            className="mb-3"
                        ),
                        html.Div([
                            html.I(className="fas fa-map-marker-alt me-2"),
                            f"Stožár {beacon_data['pole']}"
                        ], className="text-muted"),
                        html.Small(f"MAC: {beacon_data['mac']}", className="text-muted d-block mt-1")
                    ])
                ])
            ], width=12, md=4, className="mb-3")
        )
    return dbc.Row(beacon_cards)


def create_dashboard_tab():
    """Create dashboard overview tab"""
    return dbc.Container([
        dbc.Row([
            dbc.Col([
                dbc.Card([
                    dbc.CardBody([
                        html.H3("18", className="text-center text-primary"),
                        html.P("Celkem světel", className="text-center text-muted")
                    ])
                ])
            ], width=6, md=3),
            dbc.Col([
                dbc.Card([
                    dbc.CardBody([
                        html.H3("10", className="text-center text-info"),
                        html.P("Stožárů", className="text-center text-muted")
                    ])
                ])
            ], width=6, md=3),
            dbc.Col([
                dbc.Card([
                    dbc.CardBody([
                        html.H3("3", className="text-center text-warning"),
                        html.P("Majáčků", className="text-center text-muted")
                    ])
                ])
            ], width=6, md=3),
            dbc.Col([
                dbc.Card([
                    dbc.CardBody([
                        html.H3("4", className="text-center text-success"),
                        html.P("Kamer", className="text-center text-muted")
                    ])
                ])
            ], width=6, md=3),
        ], className="mb-4"),

        dbc.Row([
            dbc.Col([
                dbc.Card([
                    dbc.CardHeader("Rychlé ovládání"),
                    dbc.CardBody([
                        html.H5("Všechna světla"),
                        dbc.ButtonGroup([
                            dbc.Button("Vypnout vše", id="all-lights-off", color="danger"),
                            dbc.Button("50%", id="all-lights-50", color="warning"),
                            dbc.Button("100%", id="all-lights-100", color="success"),
                        ], className="w-100 mb-3"),

                        html.Hr(),

                        html.H5("Všechny majáčky"),
                        dbc.ButtonGroup([
                            dbc.Button("Vypnout", id="all-beacons-off", color="danger"),
                            dbc.Button("Zapnout", id="all-beacons-on", color="warning"),
                        ], className="w-100"),
                    ])
                ])
            ], width=12, md=6),

            dbc.Col([
                dbc.Card([
                    dbc.CardHeader("Systémový stav"),
                    dbc.CardBody([
                        html.Div([
                            html.Div([
                                daq.Indicator(
                                    id='system-mqtt-status',
                                    value=False,
                                    color="#00EA64",
                                    size=30
                                ),
                                html.Span("MQTT Broker", className="ms-3 h5")
                            ], className="d-flex align-items-center mb-3"),

                            html.Div([
                                html.I(className="fas fa-server fa-2x text-info me-3"),
                                html.Div([
                                    html.Strong("Server: "),
                                    html.Span("158.196.15.41:1883")
                                ])
                            ], className="d-flex align-items-center mb-2"),

                            html.Div([
                                html.I(className="fas fa-clock fa-2x text-warning me-3"),
                                html.Div([
                                    html.Strong("Čas: "),
                                    html.Span(id='current-time')
                                ])
                            ], className="d-flex align-items-center"),
                        ])
                    ])
                ])
            ], width=12, md=6),
        ]),

        dcc.Interval(id='time-update', interval=1000, n_intervals=0)
    ], fluid=True)


def create_lights_tab():
    """Create lights control tab"""
    light_cards = []
    for pole_id, pole_data in LIGHTS.items():
        light_cards.append(
            dbc.Col(
                create_light_control_card(pole_id, pole_data),
                width=12, md=6, lg=4
            )
        )

    return dbc.Container([
        html.H3("Ovládání osvětlení", className="mb-3"),
        dbc.Row(light_cards)
    ], fluid=True)


def create_beacons_tab():
    """Create beacons control tab"""
    return dbc.Container([
        html.H3("Ovládání majáčků", className="mb-3"),
        create_beacon_control()
    ], fluid=True)


def create_weather_tab():
    """Create weather station tab"""
    return dbc.Container([
        html.H3("Meteostanice GIOM 3000", className="mb-3"),

        # Connection status
        dbc.Row([
            dbc.Col([
                dbc.Card([
                    dbc.CardBody([
                        html.Div([
                            daq.Indicator(
                                id='weather-status',
                                value=False,
                                color="#00EA64",
                                size=15,
                                className="d-inline-block me-2"
                            ),
                            html.Span("Připojení k meteostanici", className="me-3"),
                            html.Code(f"{WEATHER_STATION['ip']}:{WEATHER_STATION['port']}", className="text-muted")
                        ], className="d-flex align-items-center")
                    ])
                ], className="mb-3")
            ])
        ]),

        # Weather data cards
        dbc.Row([
            # Temperature
            dbc.Col([
                dbc.Card([
                    dbc.CardHeader([
                        html.I(className="fas fa-thermometer-half me-2"),
                        "Teplota"
                    ]),
                    dbc.CardBody([
                        html.H2(id='weather-temperature', children="--", className="text-center mb-0"),
                        html.P("°C", className="text-center text-muted")
                    ])
                ])
            ], width=12, md=6, lg=3, className="mb-3"),

            # Humidity
            dbc.Col([
                dbc.Card([
                    dbc.CardHeader([
                        html.I(className="fas fa-tint me-2"),
                        "Vlhkost"
                    ]),
                    dbc.CardBody([
                        html.H2(id='weather-humidity', children="--", className="text-center mb-0"),
                        html.P("%", className="text-center text-muted")
                    ])
                ])
            ], width=12, md=6, lg=3, className="mb-3"),

            # Pressure
            dbc.Col([
                dbc.Card([
                    dbc.CardHeader([
                        html.I(className="fas fa-tachometer-alt me-2"),
                        "Tlak"
                    ]),
                    dbc.CardBody([
                        html.H2(id='weather-pressure', children="--", className="text-center mb-0"),
                        html.P("hPa", className="text-center text-muted")
                    ])
                ])
            ], width=12, md=6, lg=3, className="mb-3"),

            # Wind speed
            dbc.Col([
                dbc.Card([
                    dbc.CardHeader([
                        html.I(className="fas fa-wind me-2"),
                        "Vítr"
                    ]),
                    dbc.CardBody([
                        html.H2(id='weather-wind', children="--", className="text-center mb-0"),
                        html.P("m/s", className="text-center text-muted")
                    ])
                ])
            ], width=12, md=6, lg=3, className="mb-3"),
        ]),

        # Raw data (for debugging)
        dbc.Row([
            dbc.Col([
                dbc.Card([
                    dbc.CardHeader([
                        html.I(className="fas fa-code me-2"),
                        "Raw Data"
                    ]),
                    dbc.CardBody([
                        html.Pre(
                            id='weather-raw',
                            children="Waiting for data...",
                            style={
                                'backgroundColor': '#1a1a1a',
                                'color': '#00EA64',
                                'padding': '10px',
                                'borderRadius': '5px',
                                'fontSize': '12px',
                                'maxHeight': '200px',
                                'overflowY': 'auto'
                            }
                        )
                    ])
                ])
            ])
        ]),

        # Auto-refresh interval
        dcc.Interval(id='weather-refresh', interval=10000, n_intervals=0)  # Update every 10 seconds
    ], fluid=True)


def create_cameras_tab():
    """Create cameras view tab"""
    camera_cards = []
    for cam_id, cam_data in CAMERAS.items():
        # Check if camera has IP configured
        has_feed = cam_data.get('ip') is not None

        if has_feed:
            # Camera with live feed
            camera_content = html.Div([
                html.Img(
                    id={'type': 'camera-feed', 'id': cam_id},
                    src='',
                    style={
                        'width': '100%',
                        'maxHeight': '400px',
                        'objectFit': 'contain',
                        'borderRadius': '5px',
                        'backgroundColor': '#000'
                    }
                ),
                html.Div([
                    daq.Indicator(
                        id={'type': 'camera-status', 'id': cam_id},
                        value=True,
                        color="#00EA64",
                        size=15,
                        className="d-inline-block me-2"
                    ),
                    html.Small("Live", className="text-success")
                ], className="mt-2 text-center")
            ])
        else:
            # Placeholder for unconfigured camera
            camera_content = html.Div([
                html.I(className="fas fa-camera fa-5x text-muted")
            ], className="text-center p-4 bg-dark rounded")

        camera_cards.append(
            dbc.Col([
                dbc.Card([
                    dbc.CardHeader([
                        html.I(className="fas fa-video me-2"),
                        cam_data['name']
                    ]),
                    dbc.CardBody([
                        camera_content,
                        html.Div([
                            html.P([
                                html.I(className="fas fa-map-marker-alt me-2"),
                                cam_data['location']
                            ], className="mb-1 mt-3"),
                            html.P([
                                html.I(className="fas fa-traffic-light me-2"),
                                f"Stožár {cam_data['pole']}"
                            ], className="mb-0 text-muted")
                        ])
                    ])
                ])
            ], width=12, md=6, lg=6, className="mb-3")
        )

    return dbc.Container([
        html.H3("Kamery", className="mb-3"),
        dbc.Row(camera_cards),
        # Interval for camera refresh
        dcc.Interval(id='camera-refresh', interval=1000, n_intervals=0)
    ], fluid=True)


# ============= MAIN LAYOUT =============

app.layout = html.Div([
    create_navbar(),
    dbc.Container([
        dbc.Tabs([
            dbc.Tab(create_dashboard_tab(), label="Dashboard", tab_id="dashboard",
                   label_style={"cursor": "pointer"}),
            dbc.Tab(create_lights_tab(), label="Osvětlení", tab_id="lights",
                   label_style={"cursor": "pointer"}),
            dbc.Tab(create_beacons_tab(), label="Majáčky", tab_id="beacons",
                   label_style={"cursor": "pointer"}),
            dbc.Tab(create_weather_tab(), label="Meteostanice", tab_id="weather",
                   label_style={"cursor": "pointer"}),
            dbc.Tab(create_cameras_tab(), label="Kamery", tab_id="cameras",
                   label_style={"cursor": "pointer"}),
        ], id="tabs", active_tab="dashboard")
    ], fluid=True, className="mb-4"),

    # Store for device states from MQTT
    dcc.Store(id='device-states', data={}),

    # Interval to sync MQTT states
    dcc.Interval(id='mqtt-sync', interval=2000, n_intervals=0)
])


# ============= CALLBACKS =============

@app.callback(
    [Output('mqtt-status', 'value'),
     Output('system-mqtt-status', 'value')],
    Input('time-update', 'n_intervals')
)
def update_mqtt_status(n):
    """Update MQTT connection status"""
    status = mqtt_client.connected
    return status, status


@app.callback(
    Output('current-time', 'children'),
    Input('time-update', 'n_intervals')
)
def update_time(n):
    """Update current time"""
    return datetime.now().strftime('%H:%M:%S')


@app.callback(
    Output('device-states', 'data'),
    Input('mqtt-sync', 'n_intervals')
)
def sync_mqtt_states(n):
    """Sync MQTT device states to store"""
    # Request status on first run
    if n == 0:
        for pole_id, pole_data in LIGHTS.items():
            for device in pole_data['devices']:
                mqtt_client.get_light_power(device['mac'], device['segment'])

    states = {}

    # Extract power states from MQTT client
    for topic, value in mqtt_client.device_states.items():
        if '/power' in topic and '/power/' not in topic:
            # Parse topic: lights/device/{mac}/segment/{segment}/power
            parts = topic.split('/')
            if len(parts) >= 5:
                mac = parts[2]
                segment = parts[4]
                key = f"{mac}_{segment}"
                try:
                    states[key] = float(value)
                except (ValueError, TypeError):
                    pass

    return states


@app.callback(
    Output('tabs', 'active_tab'),
    Input('tabs', 'active_tab'),
    prevent_initial_call=True
)
def request_status_on_tab_change(active_tab):
    """Request device status when switching to lights tab"""
    if active_tab == "lights":
        # Request status for all lights
        for pole_id, pole_data in LIGHTS.items():
            for device in pole_data['devices']:
                mqtt_client.get_light_power(device['mac'], device['segment'])

    return active_tab


@app.callback(
    Output({'type': 'light-slider', 'pole': MATCH, 'device': MATCH}, 'value'),
    [Input({'type': 'light-off-btn', 'pole': MATCH, 'device': MATCH}, 'n_clicks'),
     Input({'type': 'light-50-btn', 'pole': MATCH, 'device': MATCH}, 'n_clicks'),
     Input({'type': 'light-100-btn', 'pole': MATCH, 'device': MATCH}, 'n_clicks'),
     Input({'type': 'light-slider', 'pole': MATCH, 'device': MATCH}, 'value'),
     Input('device-states', 'data')],
    State({'type': 'light-slider', 'pole': MATCH, 'device': MATCH}, 'id'),
    prevent_initial_call=True
)
def control_single_light(off_clicks, fifty_clicks, hundred_clicks, slider_val, device_states, component_id):
    """Control individual light and sync with MQTT state"""
    ctx = callback_context
    if not ctx.triggered:
        return slider_val

    trigger = ctx.triggered[0]
    prop_id = trigger['prop_id']

    pole_id = component_id['pole']
    device_idx = component_id['device']

    # Get device MAC address
    device = LIGHTS[pole_id]['devices'][device_idx]
    mac = device['mac']
    segment = device['segment']

    # Check if triggered by device-states update
    if 'device-states' in prop_id:
        # Update slider from MQTT state
        state_key = f"{mac}_{segment}"
        if device_states and state_key in device_states:
            return device_states[state_key]
        return slider_val

    new_value = slider_val

    if 'off-btn' in prop_id:
        new_value = 0
    elif '50-btn' in prop_id:
        new_value = 50
    elif '100-btn' in prop_id:
        new_value = 100

    # Send MQTT command
    mqtt_client.set_light_power(mac, segment, new_value)

    return new_value


@app.callback(
    Output('all-lights-off', 'n_clicks'),
    Input('all-lights-off', 'n_clicks'),
    prevent_initial_call=True
)
def turn_off_all_lights(n_clicks):
    """Turn off all lights"""
    if n_clicks:
        for pole_id, pole_data in LIGHTS.items():
            for device in pole_data['devices']:
                mqtt_client.set_light_power(device['mac'], device['segment'], 0)
    return 0


@app.callback(
    Output('all-lights-50', 'n_clicks'),
    Input('all-lights-50', 'n_clicks'),
    prevent_initial_call=True
)
def set_all_lights_50(n_clicks):
    """Set all lights to 50%"""
    if n_clicks:
        for pole_id, pole_data in LIGHTS.items():
            for device in pole_data['devices']:
                mqtt_client.set_light_power(device['mac'], device['segment'], 50)
    return 0


@app.callback(
    Output('all-lights-100', 'n_clicks'),
    Input('all-lights-100', 'n_clicks'),
    prevent_initial_call=True
)
def turn_on_all_lights(n_clicks):
    """Turn on all lights to 100%"""
    if n_clicks:
        for pole_id, pole_data in LIGHTS.items():
            for device in pole_data['devices']:
                mqtt_client.set_light_power(device['mac'], device['segment'], 100)
    return 0


@app.callback(
    Output({'type': 'beacon-switch', 'id': MATCH}, 'on'),
    Input({'type': 'beacon-switch', 'id': MATCH}, 'on'),
    State({'type': 'beacon-switch', 'id': MATCH}, 'id'),
    prevent_initial_call=True
)
def control_beacon(on, component_id):
    """Control beacon"""
    beacon_id = component_id['id']
    beacon = BEACONS[beacon_id]
    mqtt_client.set_beacon(beacon['mac'], on)
    return on


@app.callback(
    Output('all-beacons-off', 'n_clicks'),
    Input('all-beacons-off', 'n_clicks'),
    prevent_initial_call=True
)
def turn_off_all_beacons(n_clicks):
    """Turn off all beacons"""
    if n_clicks:
        for beacon_id, beacon_data in BEACONS.items():
            mqtt_client.set_beacon(beacon_data['mac'], False)
    return 0


@app.callback(
    Output('all-beacons-on', 'n_clicks'),
    Input('all-beacons-on', 'n_clicks'),
    prevent_initial_call=True
)
def turn_on_all_beacons(n_clicks):
    """Turn on all beacons"""
    if n_clicks:
        for beacon_id, beacon_data in BEACONS.items():
            mqtt_client.set_beacon(beacon_data['mac'], True)
    return 0


@app.callback(
    Output({'type': 'camera-feed', 'id': ALL}, 'src'),
    Input('camera-refresh', 'n_intervals')
)
def update_camera_feeds(n):
    """Update camera image sources"""
    camera_srcs = []
    # Only return sources for cameras that have IP configured (and thus have feed components)
    for cam_id, cam_data in CAMERAS.items():
        if cam_data.get('ip'):
            # Add timestamp to prevent caching
            camera_srcs.append(f'/camera/{cam_id}/snapshot?t={n}')
    return camera_srcs


# ============= WEATHER STATION CALLBACKS =============

@app.callback(
    [Output('weather-status', 'value'),
     Output('weather-temperature', 'children'),
     Output('weather-humidity', 'children'),
     Output('weather-pressure', 'children'),
     Output('weather-wind', 'children'),
     Output('weather-raw', 'children')],
    Input('weather-refresh', 'n_intervals')
)
def update_weather_data(n):
    """Fetch and update weather station data"""
    print(f"\n{'='*50}")
    print(f"[CALLBACK] Weather update triggered (n={n})")
    print(f"{'='*50}")

    # Fetch data from weather station
    data = weather_client.connect_and_read()

    if data and weather_client.connected:
        # Extract values with defaults
        temp = data.get('temperature', '--')
        humidity = data.get('humidity', '--')
        pressure = data.get('pressure', '--')
        wind = data.get('wind_speed', '--')
        raw = data.get('raw', 'No data')

        # Format values
        temp_str = f"{temp:.1f}" if isinstance(temp, (int, float)) else str(temp)
        humidity_str = f"{humidity:.0f}" if isinstance(humidity, (int, float)) else str(humidity)
        pressure_str = f"{pressure:.1f}" if isinstance(pressure, (int, float)) else str(pressure)
        wind_str = f"{wind:.1f}" if isinstance(wind, (int, float)) else str(wind)

        return True, temp_str, humidity_str, pressure_str, wind_str, raw
    else:
        return False, "--", "--", "--", "--", "Connection failed or no data received"


# ============= APP STARTUP =============

if __name__ == '__main__':
    # Connect to MQTT broker
    print("Connecting to MQTT broker...")
    if mqtt_client.connect():
        print("✓ Connected to MQTT broker")
    else:
        print("✗ Failed to connect to MQTT broker")
        print("  The app will still run but without MQTT functionality")

    # Run the app
    host = os.getenv('DASH_HOST', '0.0.0.0')
    port = int(os.getenv('DASH_PORT', 8050))
    debug = os.getenv('DASH_DEBUG', 'False').lower() == 'true'

    print(f"\nStarting Dash server on {host}:{port}")
    print(f"Access the app at: http://localhost:{port}")

    app.run(host=host, port=port, debug=debug)

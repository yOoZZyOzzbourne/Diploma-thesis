from dash import html, dcc
from .toolkit.components.sidebar import sidebar
from .toolkit.components.camera_panel import camera_panel


def login_modal():
    return html.Div([
        html.Div([
            html.Div("Přihlášení", style={"fontWeight": "700", "fontSize": "20px", "marginBottom": "20px"}),
            dcc.Input(id="login-username", type="text",    placeholder="Uživatelské jméno",
                      className="login-input", autoComplete="off", debounce=False),
            dcc.Input(id="login-password", type="password", placeholder="Heslo",
                      className="login-input", debounce=False),
            html.Div(id="login-error", style={"color": "var(--danger)", "fontSize": "13px",
                                              "marginBottom": "10px", "minHeight": "18px"}),
            html.Button("Přihlásit", id="login-submit-btn", className="action-btn accent",
                        style={"width": "100%"}, n_clicks=0),
            html.Button("Zrušit", id="login-cancel-btn", className="action-btn",
                        style={"width": "100%", "marginTop": "8px"}, n_clicks=0),
        ], className="login-box"),
    ], id="login-modal", className="login-overlay",
       style={"display": "none"})


def build_layout():
    return html.Div([
        dcc.Location(id="url", refresh=False),

        # App state stores
        dcc.Store(id="auth-store",         data={"role": "admin"}),
        dcc.Store(id="camera-panel-store", data={"open": True, "pinned": [1]}),
        dcc.Store(id="device-states",      data={}),
        dcc.Store(id="event-log-store",    data=[]),
        dcc.Store(id="modal-open",         data=False),
        dcc.Store(id="sidebar-open",       data=True),

        # Intervals
        dcc.Interval(id="mqtt-sync",      interval=2000,  n_intervals=0),
        dcc.Interval(id="camera-refresh", interval=3000,  n_intervals=0),
        dcc.Interval(id="weather-refresh",interval=10000, n_intervals=0),

        # Login modal
        login_modal(),

        # Shell
        html.Div([
            html.Div(id="sidebar-container"),
            html.Div(id="page-content", style={"flex": "1", "overflowY": "auto",
                                               "overflowX": "hidden", "padding": "28px 32px"}),
            html.Div(id="camera-panel-container"),
        ], id="app-shell"),
    ])

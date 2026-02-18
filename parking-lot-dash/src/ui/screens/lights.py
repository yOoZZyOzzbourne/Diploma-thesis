from dash import html
from config.devices import LIGHTS
from ..toolkit.components.light_card import light_card


def lights_screen(is_admin: bool = False):
    disabled = not is_admin

    bulk_bar = html.Div([
        html.Div([
            html.I(className="fas fa-bolt me-2", style={"color": "var(--accent)"}),
            html.Div([
                html.Div("HROMADNÉ AKCE", style={"fontSize": "10px", "letterSpacing": "0.1em",
                                                  "color": "var(--text-secondary)", "fontWeight": "600"}),
                html.Div("Aplikovat na celou zónu", style={"fontSize": "13px", "fontWeight": "600"}),
            ]),
        ], style={"display": "flex", "alignItems": "center", "gap": "10px"}),

        html.Div([
            html.Button("OFF (0%)", id="bulk-off", className="action-btn danger", disabled=disabled, n_clicks=0),
            html.Button("DIM (50%)", id="bulk-50", className="action-btn", disabled=disabled, n_clicks=0),
            html.Button("FULL (100%)", id="bulk-100", className="action-btn accent", disabled=disabled, n_clicks=0),
        ], style={"display": "flex", "gap": "8px"}),
    ], className="park-card",
       style={"display": "flex", "justifyContent": "space-between", "alignItems": "center",
              "marginBottom": "24px"})

    cards = html.Div([
        light_card(pole_id, pole_data, is_admin)
        for pole_id, pole_data in LIGHTS.items()
    ], style={"display": "grid",
              "gridTemplateColumns": "repeat(auto-fill, minmax(240px, 1fr))",
              "gap": "16px"})

    return html.Div([
        html.Div([
            html.Div([
                html.I(className="fas fa-lightbulb me-2", style={"color": "var(--accent)"}),
                html.Span("Správa Osvětlení"),
            ], className="screen-title"),
            html.Div("Monitoring a ovládání 10 světelných bodů v Zóně A.", className="screen-subtitle"),
        ], style={"marginBottom": "24px"}),

        bulk_bar,
        cards,
    ])

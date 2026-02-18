from dash import html
from ..toolkit.components.stat_card import stat_card
from ..toolkit.components.pole_map import pole_map
from ..toolkit.components.event_log import event_log


def dashboard_screen():
    stats = html.Div([
        stat_card("Světla aktivní",   "stat-lights-active",  "—",  "z 18",  "fas fa-lightbulb"),
        stat_card("Majáčky online",   "stat-beacons-online", "—",  "z 3",   "fas fa-bell"),
        stat_card("Teplota",          "stat-temperature",    "—",  "°C",    "fas fa-thermometer-half"),
        stat_card("Vlhkost",          "stat-humidity",       "—",  "%",     "fas fa-droplet"),
    ], style={"display": "grid", "gridTemplateColumns": "repeat(4, 1fr)",
              "gap": "16px", "marginBottom": "28px"})

    map_section = html.Div([
        html.Div([
            html.Div([
                html.I(className="fas fa-signal me-2", style={"color": "var(--accent)"}),
                html.Span("Live Grid — Parkoviště",
                          style={"fontWeight": "700", "fontSize": "16px"}),
            ], style={"display": "flex", "alignItems": "center"}),
        ], style={"marginBottom": "8px"}),
        pole_map(),
    ], className="park-card", style={"marginBottom": "28px"})

    log_section = html.Div([
        html.Div([
            html.Span("Systémové události",
                      style={"fontWeight": "700", "fontSize": "16px"}),
        ], style={"marginBottom": "14px"}),
        event_log(),
    ], className="park-card")

    return html.Div([
        html.Div([
            html.Div("Dashboard", className="screen-title"),
            html.Div("Přehled systému parkoviště VŠB-TUO", className="screen-subtitle"),
        ], style={"marginBottom": "24px"}),

        stats,
        map_section,
        log_section,
    ])

from dash import html

_NAV = [
    ("/",          "fas fa-grip",      "Dashboard"),
    ("/osvetleni", "fas fa-lightbulb", "Osvětlení"),
    ("/majacky",   "fas fa-bell",      "Majáčky"),
    ("/meteo",     "fas fa-cloud",     "Meteostanice"),
    ("/kamery",    "fas fa-video",     "Kamery"),
]


def sidebar(current_path: str = "/", is_admin: bool = False, mqtt_connected: bool = False):
    nav_items = []
    for path, icon, label in _NAV:
        active = current_path == path or (path != "/" and current_path.startswith(path))
        nav_items.append(
            html.A([
                html.I(className=icon, style={"width": "18px", "textAlign": "center", "flexShrink": "0"}),
                html.Span(label, className="nav-text"),
            ],
            href=path,
            className=f"nav-link-item {'active' if active else ''}",
            )
        )

    mqtt_dot_color = "var(--accent)" if mqtt_connected else "var(--danger)"
    mqtt_label = "Broker připojen" if mqtt_connected else "Broker odpojen"

    # Use html.Button (not <a href="#">) to avoid triggering URL changes
    if is_admin:
        auth_btn = html.Button([
            html.I(className="fas fa-right-from-bracket",
                   style={"width": "18px", "textAlign": "center", "color": "var(--danger)", "flexShrink": "0"}),
            html.Span("Odhlásit", className="nav-text", style={"color": "var(--danger)"}),
        ], id="logout-btn", className="nav-link-item", n_clicks=0,
           style={"background": "none", "border": "none", "width": "100%", "textAlign": "left", "cursor": "pointer"})
    else:
        auth_btn = html.Button([
            html.I(className="fas fa-right-to-bracket",
                   style={"width": "18px", "textAlign": "center", "flexShrink": "0"}),
            html.Span("Přihlásit", className="nav-text"),
        ], id="login-open-btn", className="nav-link-item", n_clicks=0,
           style={"background": "none", "border": "none", "width": "100%", "textAlign": "left", "cursor": "pointer"})

    return html.Div([
        # Logo
        html.Div([
            html.I(className="fas fa-shield-halved",
                   style={"color": "var(--accent)", "fontSize": "22px", "flexShrink": "0"}),
            html.Div([
                html.Div("Smart Parking", className="nav-text",
                         style={"fontWeight": "700", "fontSize": "15px", "color": "var(--text-primary)"}),
                html.Div("VŠB-TUO", className="nav-text",
                         style={"fontSize": "11px", "color": "var(--text-secondary)"}),
            ]),
        ], style={"display": "flex", "alignItems": "center", "gap": "10px",
                  "padding": "20px 20px 16px", "borderBottom": "1px solid var(--border)"}),

        # Nav
        html.Nav(nav_items, style={"padding": "10px 0", "flex": "1", "overflowY": "auto"}),

        # Bottom
        html.Div([
            # MQTT status dot — fixed ID, updated by separate callback
            html.Div([
                html.Div(id="mqtt-status-dot",
                         style={"width": "8px", "height": "8px", "borderRadius": "50%",
                                "background": mqtt_dot_color, "flexShrink": "0"}),
                html.Span(mqtt_label, className="nav-text",
                          style={"fontSize": "12px", "color": "var(--text-secondary)"}),
            ], style={"display": "flex", "alignItems": "center", "gap": "8px",
                      "padding": "10px 20px", "borderTop": "1px solid var(--border)"}),

            auth_btn,

            html.A([
                html.I(className="fas fa-gear",
                       style={"width": "18px", "textAlign": "center", "flexShrink": "0"}),
                html.Span("Nastavení", className="nav-text"),
            ], href="/nastaveni", className="nav-link-item"),
        ]),

        # Collapse toggle — right-edge tab
        html.Div(
            html.I(className="fas fa-chevron-left", id="sidebar-arrow-icon"),
            id="sidebar-toggle-btn",
            n_clicks=0,
            title="Sbalit / rozbalit",
        ),
    ], id="sidebar")

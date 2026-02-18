from dash import html

# Physical layout of poles on the parking lot
# Based on thesis map — two outer rows + inner cluster
_ROWS = [
    [1, 2, 3, 4],
    [5, 6, 7],
    [8, 9, 10],
]


def pole_map(online_poles: set = None):
    if online_poles is None:
        online_poles = set()  # assume offline until MQTT confirms

    rows = []
    for row in _ROWS:
        circles = []
        for pole_id in row:
            is_online = pole_id in online_poles
            circles.append(
                html.Div(
                    str(pole_id),
                    id={"type": "pole-map-circle", "pole": pole_id},
                    className=f"pole-circle {'offline' if not is_online else ''}",
                    title=f"Stožár {pole_id} — {'online' if is_online else 'offline'}",
                    n_clicks=0,
                )
            )
        rows.append(
            html.Div(circles, style={"display": "flex", "gap": "16px", "justifyContent": "center"})
        )

    legend = html.Div([
        html.Div([
            html.Div(style={"width": "12px", "height": "12px", "borderRadius": "50%",
                            "border": "2px solid var(--accent)", "display": "inline-block"}),
            html.Span("Aktivní", style={"fontSize": "12px", "color": "var(--text-secondary)", "marginLeft": "6px"}),
        ], style={"display": "flex", "alignItems": "center", "marginRight": "16px"}),
        html.Div([
            html.Div(style={"width": "12px", "height": "12px", "borderRadius": "50%",
                            "border": "2px solid var(--danger)", "display": "inline-block"}),
            html.Span("Offline / Chyba", style={"fontSize": "12px", "color": "var(--text-secondary)", "marginLeft": "6px"}),
        ], style={"display": "flex", "alignItems": "center"}),
    ], style={"display": "flex", "marginTop": "16px", "justifyContent": "flex-end"})

    return html.Div([
        html.Div(rows, style={"display": "flex", "flexDirection": "column", "gap": "20px", "padding": "24px 0"}),
        legend,
    ])

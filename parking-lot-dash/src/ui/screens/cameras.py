from dash import html
from config.devices import CAMERAS
from ..toolkit.components.camera_card import camera_card


def cameras_screen(pinned_cam_ids: list = None):
    pinned_cam_ids = pinned_cam_ids or []
    configured_count = sum(1 for c in CAMERAS.values() if c.get("ip"))
    total = len(CAMERAS)

    grid = html.Div([
        camera_card(cam_id, cam_data, is_pinned=(cam_id in pinned_cam_ids))
        for cam_id, cam_data in CAMERAS.items()
    ], style={"display": "grid", "gridTemplateColumns": "repeat(2, 1fr)", "gap": "16px"})

    footer = html.Div([
        html.Div([
            html.I(className="fas fa-signal me-2", style={"color": "var(--accent)", "fontSize": "18px"}),
            html.Div([
                html.Div("NETWORK INTEGRITY", style={"fontWeight": "700", "fontSize": "13px",
                                                      "letterSpacing": "0.06em"}),
                html.Div(f"{configured_count} z {total} jednotek komunikuje úspěšně.",
                         style={"fontSize": "12px", "color": "var(--text-secondary)"}),
            ]),
        ], style={"display": "flex", "alignItems": "center", "gap": "12px"}),

        html.Button("Obnovit vše", id="cam-refresh-btn", className="action-btn", n_clicks=0),
    ], className="park-card",
       style={"display": "flex", "justifyContent": "space-between", "alignItems": "center",
              "marginTop": "20px"})

    return html.Div([
        html.Div([
            html.Div([
                html.I(className="fas fa-video me-2", style={"color": "var(--accent)"}),
                html.Span("Live Monitor"),
            ], className="screen-title"),
            html.Div("Kamerový systém — přehled všech jednotek.", className="screen-subtitle"),
        ], style={"marginBottom": "24px"}),

        grid,
        footer,
    ])

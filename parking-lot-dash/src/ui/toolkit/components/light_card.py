from dash import html, dcc
from .status_badge import status_badge


def light_card(pole_id: int, pole_data: dict, is_admin: bool = False):
    device_type = pole_data["devices"][0]["type"]
    disabled = not is_admin

    return html.Div([
        # Header
        html.Div([
            html.Div([
                html.I(className="fas fa-lightbulb me-2", style={"color": "var(--accent)"}),
                html.Span(f"POLE-{pole_id:02d}", style={"fontWeight": "700", "fontSize": "15px"}),
            ], style={"display": "flex", "alignItems": "center"}),
            html.Div(status_badge(False), id={"type": "light-status", "pole": pole_id}),
        ], style={"display": "flex", "justifyContent": "space-between", "alignItems": "center", "marginBottom": "4px"}),

        # Device type
        html.Div(device_type, style={"color": "var(--text-secondary)", "fontSize": "12px", "marginBottom": "14px"}),

        # Current value display
        html.Div([
            html.Span("0", id={"type": "light-value", "pole": pole_id},
                      style={"fontSize": "36px", "fontWeight": "800", "color": "var(--text-primary)"}),
            html.Span(" %", style={"fontSize": "16px", "color": "var(--text-secondary)"}),
        ], style={"marginBottom": "14px"}),

        # Slider
        html.Div(
            dcc.Slider(
                id={"type": "light-slider", "pole": pole_id},
                min=0, max=100, step=1, value=0,
                marks=None,
                tooltip={"always_visible": False},
                disabled=disabled,
                className="light-slider",
            ),
            className="slider-container", style={"marginBottom": "12px"}
        ),

        # Quick buttons
        html.Div([
            html.Button("OFF", id={"type": "light-off", "pole": pole_id},
                        className="action-btn danger", disabled=disabled,
                        style={"flex": "1"}),
            html.Button("50%", id={"type": "light-50", "pole": pole_id},
                        className="action-btn", disabled=disabled,
                        style={"flex": "1"}),
            html.Button("100%", id={"type": "light-100", "pole": pole_id},
                        className="action-btn accent", disabled=disabled,
                        style={"flex": "1"}),
        ], style={"display": "flex", "gap": "6px"}),

    ], id={"type": "light-card", "pole": pole_id},
       className="park-card",
       style={"position": "relative"})

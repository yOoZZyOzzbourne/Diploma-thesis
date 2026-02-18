from dash import html
from .status_badge import configured_badge


def camera_card(cam_id: int, cam_data: dict, is_pinned: bool = False):
    configured = cam_data.get("ip") is not None
    name = cam_data["name"]
    location = cam_data["location"]
    ip = cam_data.get("ip") or "—"

    thumbnail = (
        html.Img(
            id={"type": "cam-thumb", "id": cam_id},
            src=f"/camera/{cam_id}/snapshot",
            className="cam-thumb",
        )
        if configured else
        html.Div(html.I(className="fas fa-video-slash"), className="cam-thumb-placeholder")
    )

    pin_btn = html.Button(
        [html.I(className="fas fa-thumbtack me-2"), "Připnuto" if is_pinned else "Připnout"],
        id={"type": "cam-pin-btn", "id": cam_id},
        className=f"action-btn {'accent' if is_pinned else ''}",
        style={"fontSize": "13px"},
        n_clicks=0,
    )

    return html.Div([
        # Thumbnail with overlays
        html.Div([
            thumbnail,
            html.Div([
                html.Span(
                    [html.I(className="fas fa-wifi me-1"), ip],
                    style={"fontSize": "11px", "color": "var(--text-secondary)"}
                ),
            ], style={"position": "absolute", "bottom": "8px", "left": "8px"}),
            html.Div([
                configured_badge(configured),
                html.Span(" "),
                html.Span("Připnuto", className="badge-info") if is_pinned else html.Span(),
            ], style={"position": "absolute", "top": "8px", "left": "8px", "display": "flex", "gap": "4px"}),
        ], style={"position": "relative", "marginBottom": "14px"}),

        # Name + location
        html.Div(name, style={"fontWeight": "700", "fontSize": "15px", "marginBottom": "2px"}),
        html.Div([
            html.I(className="fas fa-location-dot me-1", style={"color": "var(--text-secondary)"}),
            html.Span(location, style={"color": "var(--text-secondary)", "fontSize": "12px"}),
        ], style={"marginBottom": "14px"}),

        # Stats row
        html.Div([
            html.Div([
                html.Div("STAV", style={"fontSize": "10px", "color": "var(--text-secondary)", "letterSpacing": "0.08em"}),
                html.Div("AKTIVNÍ" if configured else "NONE",
                         style={"fontWeight": "600", "fontSize": "13px",
                                "color": "var(--accent)" if configured else "var(--text-secondary)"}),
            ]),
            html.Div(pin_btn, style={"marginLeft": "auto"}),
        ], style={"display": "flex", "alignItems": "flex-end"}),

    ], className=f"park-card {'pinned' if is_pinned else ''}")

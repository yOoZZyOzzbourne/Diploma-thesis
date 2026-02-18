from dash import html
from config.devices import CAMERAS


def camera_panel(pinned_cam_ids: list = None, is_open: bool = True):
    pinned_cam_ids = pinned_cam_ids or []

    chevron = "fa-chevron-right" if is_open else "fa-chevron-left"

    # Spine — always 36px wide, always visible, click anywhere to toggle
    spine = html.Div([
        html.I(className=f"fas {chevron}", style={"fontSize": "9px"}),
        html.I(className="fas fa-video", style={"fontSize": "13px"}),
        html.Div("LIVE", style={"writingMode": "vertical-rl", "transform": "rotate(180deg)",
                                "fontSize": "9px", "letterSpacing": "0.12em", "userSelect": "none"}),
    ], id="panel-toggle-btn", n_clicks=0, title="Skrýt / zobrazit panel")

    # Header
    n = len(pinned_cam_ids)
    count_label = f"{n}\u00a0{'kamera' if n == 1 else 'kamery' if 2 <= n <= 4 else 'kamer'}" if n else None

    header = html.Div([
        html.Div([
            html.I(className="fas fa-video me-2", style={"color": "var(--accent)"}),
            html.Span("LIVE FEED", style={"fontWeight": "700", "fontSize": "13px",
                                          "letterSpacing": "0.06em", "color": "var(--text-primary)"}),
        ], style={"display": "flex", "alignItems": "center"}),
        html.Span(count_label, style={"fontSize": "11px", "color": "var(--text-secondary)"}) if count_label else html.Span(),
    ], style={"display": "flex", "justifyContent": "space-between", "alignItems": "center",
              "padding": "12px 14px", "borderBottom": "1px solid var(--border)", "flexShrink": "0"})

    # Camera list or empty state
    if pinned_cam_ids:
        feed_area = html.Div(
            [_cam_item(cam_id) for cam_id in pinned_cam_ids],
            style={"overflowY": "auto", "flex": "1"},
        )
    else:
        feed_area = html.Div([
            html.I(className="fas fa-video-slash",
                   style={"fontSize": "28px", "color": "var(--text-secondary)", "marginBottom": "10px"}),
            html.Div("Připněte kameru", style={"fontSize": "12px", "color": "var(--text-secondary)"}),
            html.Div("tlačítkem Připnout", style={"fontSize": "11px", "color": "var(--text-secondary)",
                                                   "opacity": "0.6"}),
        ], style={"display": "flex", "flexDirection": "column", "alignItems": "center",
                  "justifyContent": "center", "flex": "1", "padding": "24px 16px"})

    content = html.Div([header, feed_area], id="camera-panel-content")

    return html.Div([
        spine,
        content,
    ], id="camera-panel", className=f"{'panel-open' if is_open else 'panel-closed'}")


def _cam_item(cam_id: int):
    cam = CAMERAS.get(cam_id, {})
    name = cam.get("name", f"Kamera {cam_id}")
    location = cam.get("location", "—")
    configured = cam.get("ip") is not None

    if configured:
        thumb = html.Img(
            id={"type": "bar-cam-img", "id": cam_id},
            src=f"/camera/{cam_id}/snapshot",
            style={"width": "100%", "aspectRatio": "16/9", "objectFit": "cover",
                   "display": "block", "background": "#000"},
        )
    else:
        thumb = html.Div(
            html.I(className="fas fa-video-slash",
                   style={"fontSize": "24px", "color": "var(--text-secondary)"}),
            style={"width": "100%", "aspectRatio": "16/9", "background": "var(--surface-variant)",
                   "display": "flex", "alignItems": "center", "justifyContent": "center"},
        )

    return html.Div([
        thumb,
        html.Div([
            html.Div([
                html.Div(name, style={"fontWeight": "600", "fontSize": "12px",
                                      "whiteSpace": "nowrap", "overflow": "hidden",
                                      "textOverflow": "ellipsis"}),
                html.Div([
                    html.I(className="fas fa-location-dot me-1",
                           style={"color": "var(--text-secondary)", "fontSize": "10px"}),
                    html.Span(location, style={"color": "var(--text-secondary)", "fontSize": "11px"}),
                ]),
            ], style={"flex": "1", "overflow": "hidden"}),
            html.Div([
                html.A(
                    html.I(className="fas fa-expand", style={"fontSize": "11px"}),
                    href=f"/camera/{cam_id}/snapshot",
                    target="_blank",
                    title="Otevřít v novém okně",
                    style={"color": "var(--text-secondary)", "textDecoration": "none",
                           "padding": "3px 6px"},
                ) if configured else html.Span(),
                html.Div(
                    html.I(className="fas fa-xmark", style={"fontSize": "11px"}),
                    id={"type": "cam-unpin-btn", "id": cam_id},
                    n_clicks=0,
                    title="Odepnout",
                    style={"color": "var(--text-secondary)", "cursor": "pointer",
                           "padding": "3px 6px", "borderRadius": "4px"},
                ),
            ], style={"display": "flex", "alignItems": "center", "flexShrink": "0"}),
        ], style={"display": "flex", "alignItems": "center", "gap": "8px", "padding": "8px 12px"}),
        html.Hr(style={"margin": "0", "borderColor": "var(--border)", "opacity": "1"}),
    ])

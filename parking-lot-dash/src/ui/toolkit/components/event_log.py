from dash import html
from datetime import datetime

_BADGE_STYLES = {
    "error":   {"background": "rgba(231,76,60,0.15)",  "color": "var(--danger)", "border": "1px solid rgba(231,76,60,0.3)"},
    "success": {"background": "rgba(0,200,83,0.15)",   "color": "var(--accent)", "border": "1px solid rgba(0,200,83,0.3)"},
    "info":    {"background": "rgba(0,229,255,0.10)",  "color": "var(--info)",   "border": "1px solid rgba(0,229,255,0.25)"},
    "warning": {"background": "rgba(255,160,0,0.15)",  "color": "#FFA000",       "border": "1px solid rgba(255,160,0,0.3)"},
}

_BASE_BADGE = {
    "display": "inline-block", "fontSize": "10px", "fontWeight": "700",
    "padding": "2px 7px", "borderRadius": "4px", "letterSpacing": "0.06em",
    "minWidth": "60px", "textAlign": "center", "textTransform": "uppercase",
}


def _badge(level: str):
    style = {**_BASE_BADGE, **_BADGE_STYLES.get(level, _BADGE_STYLES["info"])}
    return html.Span(level, style=style)


def _row(ts: str, level: str, message: str):
    return html.Div([
        html.Span(ts, className="event-time"),
        _badge(level),
        html.Span(message, style={"fontSize": "13px", "color": "var(--text-primary)", "flex": "1"}),
    ], className="event-row")


def event_log(events: list = None):
    """
    events: list of dicts with keys: ts (str), level (str), message (str)
    If None, renders a placeholder.
    """
    if not events:
        events = [{"ts": datetime.now().strftime("%Y-%m-%d %H:%M:%S"), "level": "info", "message": "Systém spuštěn"}]

    rows = [_row(e["ts"], e["level"], e["message"]) for e in events]

    return html.Div(rows, id="event-log-list",
                    style={"maxHeight": "260px", "overflowY": "auto"})

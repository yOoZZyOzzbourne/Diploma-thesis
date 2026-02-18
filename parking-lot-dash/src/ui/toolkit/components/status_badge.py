from dash import html


def status_badge(online: bool):
    if online:
        return html.Span([
            html.I(className="fas fa-wifi me-1"),
            "ONLINE"
        ], className="badge-online")
    return html.Span([
        html.I(className="fas fa-wifi me-1"),
        "OFFLINE"
    ], className="badge-offline")


def configured_badge(configured: bool):
    if configured:
        return html.Span("Konfigurováno", className="badge-online")
    return html.Span("Nenakonfigurováno", className="badge-offline")

from dash import html


def stat_card(label: str, value_id: str, value: str, sub: str = "", icon: str = "fas fa-circle"):
    return html.Div([
        html.Div([
            html.I(className=f"{icon}", style={"color": "var(--accent)", "fontSize": "18px"}),
            html.Span(sub, style={"color": "var(--accent)", "fontSize": "12px", "marginLeft": "auto"}),
        ], style={"display": "flex", "alignItems": "center", "marginBottom": "12px"}),
        html.Div(value, id=value_id, className="stat-value"),
        html.Div(label, className="stat-label"),
    ], className="park-card", style={"minWidth": "140px"})

from dash import Input, Output, State, callback, no_update, ctx
from flask import session

from src.ui.toolkit.components.sidebar import sidebar
from src.ui.toolkit.components.camera_panel import camera_panel
from src.ui.toolkit.components.event_log import event_log as render_event_log
from src.ui.screens.dashboard import dashboard_screen
from src.ui.screens.lights import lights_screen
from src.ui.screens.cameras import cameras_screen
from src.mqtt_client import ParkingLotMQTT


def register(mqtt_client: ParkingLotMQTT):

    # Re-renders only on real navigation events, never on intervals
    @callback(
        Output("page-content", "children"),
        Output("sidebar-container", "children"),
        Output("camera-panel-container", "children"),
        Input("url", "pathname"),
        Input("auth-store", "data"),
        Input("camera-panel-store", "data"),
    )
    def render_page(pathname, auth, panel_state):
        is_admin = auth.get("role") == "admin"
        pinned = panel_state.get("pinned", [1])
        panel_open = panel_state.get("open", True)

        nav = sidebar(
            current_path=pathname or "/",
            is_admin=is_admin,
            mqtt_connected=mqtt_client.connected,
        )
        panel = camera_panel(pinned_cam_ids=pinned, is_open=panel_open)

        if pathname == "/osvetleni":
            page = lights_screen(is_admin=is_admin)
        elif pathname == "/kamery":
            page = cameras_screen(pinned_cam_ids=pinned)
        else:
            page = dashboard_screen()

        return page, nav, panel

    # Updates only the MQTT dot — no sidebar re-render needed
    @callback(
        Output("mqtt-status-dot", "style"),
        Input("mqtt-sync", "n_intervals"),
    )
    def update_mqtt_dot(_):
        color = "var(--accent)" if mqtt_client.connected else "var(--danger)"
        return {"width": "8px", "height": "8px", "borderRadius": "50%",
                "background": color, "flexShrink": "0"}

    @callback(
        Output("sidebar-open", "data"),
        Input("sidebar-toggle-btn", "n_clicks"),
        State("sidebar-open", "data"),
        prevent_initial_call=True,
    )
    def toggle_sidebar(n_clicks, is_open):
        if (n_clicks or 0) > 0:
            return not is_open
        return no_update

    @callback(
        Output("sidebar-container", "style"),
        Output("sidebar-arrow-icon", "className"),
        Input("sidebar-open", "data"),
    )
    def apply_sidebar_state(is_open):
        if is_open:
            return {"width": "var(--sidebar-w)", "flexShrink": "0"}, "fas fa-chevron-left"
        return {"width": "64px", "flexShrink": "0"}, "fas fa-chevron-right"

    # Sync MQTT event log into the Dash store every interval tick
    @callback(
        Output("event-log-store", "data"),
        Input("mqtt-sync", "n_intervals"),
    )
    def sync_event_log(_):
        return mqtt_client.event_log[-50:]

    # Render event-log-list from the store (only active when on dashboard)
    @callback(
        Output("event-log-list", "children"),
        Input("event-log-store", "data"),
    )
    def render_log(events):
        return render_event_log(events if events else None).children

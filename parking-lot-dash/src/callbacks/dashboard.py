from dash import Input, Output, State, callback, ALL
from config.devices import LIGHTS
from src.ui.toolkit.components.status_badge import status_badge


def _to_float(v, default=0):
    try:
        return float(v)
    except (ValueError, TypeError):
        return default


def _pole_online(pole_id, device_states):
    return any(
        device_states.get(f"{dev['mac']}_status") == "online"
        for dev in LIGHTS.get(pole_id, {}).get("devices", [])
    )


def register(weather_client):

    @callback(
        Output({"type": "pole-map-circle", "pole": ALL}, "className"),
        Output({"type": "pole-map-circle", "pole": ALL}, "title"),
        Output("stat-lights-active", "children"),
        Input("device-states", "data"),
        State({"type": "pole-map-circle", "pole": ALL}, "id"),
    )
    def update_pole_map(device_states, circle_ids):
        device_states = device_states or {}
        classnames, titles = [], []
        for id_obj in circle_ids:
            pole_id = id_obj["pole"]
            online = _pole_online(pole_id, device_states)
            classnames.append("pole-circle" if online else "pole-circle offline")
            titles.append(f"Stožár {pole_id} — {'online' if online else 'offline'}")
        active = sum(1 for k, v in device_states.items()
                     if not k.endswith("_status") and _to_float(v, 0) > 0)
        return classnames, titles, str(active)

    @callback(
        Output({"type": "light-status", "pole": ALL}, "children"),
        Input("device-states", "data"),
        State({"type": "light-status", "pole": ALL}, "id"),
    )
    def update_light_badges(device_states, badge_ids):
        device_states = device_states or {}
        return [status_badge(_pole_online(id_obj["pole"], device_states)) for id_obj in badge_ids]

    @callback(
        Output("stat-temperature", "children"),
        Output("stat-humidity", "children"),
        Input("weather-refresh", "n_intervals"),
    )
    def update_weather(_):
        data = weather_client.get_last_data()
        temp = f"{data['temperature']:.1f}" if "temperature" in data else "—"
        hum  = f"{data['humidity']:.0f}"    if "humidity"    in data else "—"
        return temp, hum

from dash import Input, Output, State, callback, no_update, ALL, ctx
from flask import session
from config.devices import LIGHTS
from src.mqtt_client import ParkingLotMQTT


def _is_admin():
    return session.get("role") == "admin"


def register(mqtt_client: ParkingLotMQTT):

    @callback(
        Output("device-states", "data"),
        Input("mqtt-sync", "n_intervals"),
    )
    def sync_states(_):
        states = {}
        for topic, value in mqtt_client.device_states.items():
            parts = topic.split("/")
            if "/power" in topic and "/power/" not in topic:
                # lights/device/{mac}/segment/{seg}/power
                if len(parts) >= 5:
                    key = f"{parts[2]}_{parts[4]}"
                    try:
                        states[key] = float(value)
                    except (ValueError, TypeError):
                        pass
            elif topic.endswith("/telemetry/status"):
                # lights/device/{mac}/telemetry/status  ->  "{mac}_status"
                if len(parts) >= 4:
                    states[f"{parts[2]}_status"] = value  # "online" or "offline"
        return states

    @callback(
        Output({"type": "light-slider", "pole": ALL}, "value"),
        Output({"type": "light-value",  "pole": ALL}, "children"),
        Input({"type": "light-off",    "pole": ALL}, "n_clicks"),
        Input({"type": "light-50",     "pole": ALL}, "n_clicks"),
        Input({"type": "light-100",    "pole": ALL}, "n_clicks"),
        Input({"type": "light-slider", "pole": ALL}, "value"),
        Input("device-states", "data"),
        State({"type": "light-slider", "pole": ALL}, "id"),
        State({"type": "light-slider", "pole": ALL}, "value"),
        prevent_initial_call=True,
    )
    def control_lights(_off, _50, _100, _slider, device_states, ids, current_values):
        trigger = ctx.triggered_id
        if not trigger:
            return [no_update] * len(ids), [no_update] * len(ids)

        new_values = list(current_values)

        # Sync from MQTT states when device-states updated
        if trigger == "device-states":
            for i, id_obj in enumerate(ids):
                pole_id = id_obj["pole"]
                for dev in LIGHTS[pole_id]["devices"]:
                    key = f"{dev['mac']}_{dev['segment']}"
                    if key in device_states:
                        new_values[i] = device_states[key]
            return new_values, [str(int(v)) for v in new_values]

        if not _is_admin():
            return [no_update] * len(ids), [no_update] * len(ids)

        # Find which pole triggered
        if isinstance(trigger, dict):
            pole_id = trigger.get("pole")
            action  = trigger.get("type")
            idx = next((i for i, id_obj in enumerate(ids) if id_obj["pole"] == pole_id), None)
            if idx is None:
                return [no_update] * len(ids), [no_update] * len(ids)

            if action == "light-off":
                new_values[idx] = 0
            elif action == "light-50":
                new_values[idx] = 50
            elif action == "light-100":
                new_values[idx] = 100
            elif action == "light-slider":
                new_values[idx] = _slider[idx]

            val = new_values[idx]
            for dev in LIGHTS[pole_id]["devices"]:
                mqtt_client.set_light_power(dev["mac"], dev["segment"], val)

        return new_values, [str(int(v)) for v in new_values]

    @callback(
        Output("bulk-off",  "n_clicks"),
        Output("bulk-50",   "n_clicks"),
        Output("bulk-100",  "n_clicks"),
        Input("bulk-off",   "n_clicks"),
        Input("bulk-50",    "n_clicks"),
        Input("bulk-100",   "n_clicks"),
        prevent_initial_call=True,
    )
    def bulk_control(off, fifty, hundred):
        if not _is_admin():
            return 0, 0, 0
        trigger = ctx.triggered_id
        level = {"bulk-off": 0, "bulk-50": 50, "bulk-100": 100}.get(trigger, None)
        if level is not None:
            for pole_data in LIGHTS.values():
                for dev in pole_data["devices"]:
                    mqtt_client.set_light_power(dev["mac"], dev["segment"], level)
        return 0, 0, 0

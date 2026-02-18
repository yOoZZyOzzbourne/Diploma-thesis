from dash import Input, Output, State, callback, no_update, ALL, ctx
from config.devices import CAMERAS


def register():

    @callback(
        Output("camera-panel-store", "data"),
        Input("panel-toggle-btn", "n_clicks"),
        Input({"type": "cam-pin-btn", "id": ALL}, "n_clicks"),
        Input({"type": "cam-unpin-btn", "id": ALL}, "n_clicks"),
        State("camera-panel-store", "data"),
        State({"type": "cam-pin-btn", "id": ALL}, "id"),
        State({"type": "cam-unpin-btn", "id": ALL}, "id"),
        prevent_initial_call=True,
    )
    def update_panel_store(toggle_clicks, pin_clicks, unpin_clicks, store, pin_ids, unpin_ids):
        trigger = ctx.triggered_id

        if trigger == "panel-toggle-btn":
            return {**store, "open": not store.get("open", True)}

        if isinstance(trigger, dict) and trigger.get("type") == "cam-pin-btn":
            cam_id = trigger["id"]
            pinned = list(store.get("pinned", []))
            if cam_id in pinned:
                pinned.remove(cam_id)
                return {**store, "pinned": pinned}
            pinned.append(cam_id)
            return {**store, "open": True, "pinned": pinned}

        if isinstance(trigger, dict) and trigger.get("type") == "cam-unpin-btn":
            cam_id = trigger["id"]
            pinned = list(store.get("pinned", []))
            if cam_id in pinned:
                pinned.remove(cam_id)
            return {**store, "pinned": pinned}

        return no_update

    @callback(
        Output({"type": "bar-cam-img", "id": ALL}, "src"),
        Input("camera-refresh", "n_intervals"),
        State({"type": "bar-cam-img", "id": ALL}, "id"),
    )
    def refresh_bar_feeds(n, img_ids):
        if not img_ids:
            return []
        srcs = []
        for id_dict in img_ids:
            cam_id = id_dict["id"]
            cam = CAMERAS.get(cam_id, {})
            if cam.get("ip"):
                srcs.append(f"/camera/{cam_id}/snapshot?t={n}")
            else:
                srcs.append(no_update)
        return srcs

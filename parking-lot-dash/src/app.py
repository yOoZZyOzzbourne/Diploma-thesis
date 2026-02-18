import sys
import os
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

import dash
import dash_bootstrap_components as dbc
import requests
from requests.auth import HTTPBasicAuth, HTTPDigestAuth
from flask import Response, session

from config.devices import CAMERAS, WEATHER_STATION
from src.mqtt_client import ParkingLotMQTT
from src.weather_client import WeatherStationClient
from src.ui.layout import build_layout
import src.callbacks.routing   as routing_cb
import src.callbacks.auth      as auth_cb
import src.callbacks.lights    as lights_cb
import src.callbacks.cameras   as cameras_cb
import src.callbacks.dashboard as dashboard_cb

# ── App ──────────────────────────────────────────────────────────────────────

app = dash.Dash(
    __name__,
    external_stylesheets=[dbc.icons.FONT_AWESOME],
    suppress_callback_exceptions=True,
    title="Smart Parking — VŠB-TUO",
)
app.server.secret_key = "parking-vsb-tuo-2024"
server = app.server

# ── Clients ──────────────────────────────────────────────────────────────────

mqtt_client    = ParkingLotMQTT()
weather_client = WeatherStationClient(host=WEATHER_STATION["ip"], port=WEATHER_STATION["port"])
weather_client.start_background_polling(interval=60)

# ── Flask routes ─────────────────────────────────────────────────────────────

@server.route("/camera/<int:cam_id>/snapshot")
def camera_snapshot(cam_id):
    cam = CAMERAS.get(cam_id)
    if not cam or not cam.get("snapshot_url"):
        return "Not configured", 404
    try:
        auth = HTTPDigestAuth if cam["type"] == "axis" else HTTPBasicAuth
        r = requests.get(cam["snapshot_url"],
                         auth=auth(cam["username"], cam["password"]),
                         timeout=5, verify=False)
        if r.status_code == 200:
            return Response(r.content, mimetype="image/jpeg")
        return f"Camera error {r.status_code}", 500
    except Exception as e:
        return str(e), 500

# ── Layout & callbacks ────────────────────────────────────────────────────────

app.layout = build_layout()

routing_cb.register(mqtt_client)
auth_cb.register()
lights_cb.register(mqtt_client)
cameras_cb.register()
dashboard_cb.register(weather_client)

# ── Entry point ───────────────────────────────────────────────────────────────

if __name__ == "__main__":
    if mqtt_client.connect():
        print("MQTT connected")
    else:
        print("MQTT unavailable — running without broker")

    app.run(host="0.0.0.0", port=8050, debug=False)

from fastapi import FastAPI, Request
from fastapi.responses import HTMLResponse
from fastapi.staticfiles import StaticFiles
from fastapi.templating import Jinja2Templates
import numpy as np
from datetime import datetime
import uvicorn

app = FastAPI(title="IoT Dashboard - FastAPI + HTMX")

templates = Jinja2Templates(directory="templates")

# In-memory state (in production, use a database or Redis)
state = {
    "living_room_light": False,
    "bedroom_light": False,
    "kitchen_light": False,
    "camera_enabled": True,
}


@app.get("/", response_class=HTMLResponse)
async def read_root(request: Request):
    """Render the main dashboard page."""
    return templates.TemplateResponse("index.html", {"request": request, "state": state})


@app.post("/toggle/living_room")
async def toggle_living_room(request: Request):
    """Toggle living room light."""
    state["living_room_light"] = not state["living_room_light"]
    return templates.TemplateResponse(
        "light_switch.html",
        {
            "request": request,
            "name": "Living Room",
            "id": "living_room",
            "is_on": state["living_room_light"]
        }
    )


@app.post("/toggle/bedroom")
async def toggle_bedroom(request: Request):
    """Toggle bedroom light."""
    state["bedroom_light"] = not state["bedroom_light"]
    return templates.TemplateResponse(
        "light_switch.html",
        {
            "request": request,
            "name": "Bedroom",
            "id": "bedroom",
            "is_on": state["bedroom_light"]
        }
    )


@app.post("/toggle/kitchen")
async def toggle_kitchen(request: Request):
    """Toggle kitchen light."""
    state["kitchen_light"] = not state["kitchen_light"]
    return templates.TemplateResponse(
        "light_switch.html",
        {
            "request": request,
            "name": "Kitchen",
            "id": "kitchen",
            "is_on": state["kitchen_light"]
        }
    )


@app.post("/toggle/camera")
async def toggle_camera(request: Request):
    """Toggle camera."""
    state["camera_enabled"] = not state["camera_enabled"]
    return templates.TemplateResponse(
        "camera_status.html",
        {"request": request, "camera_enabled": state["camera_enabled"]}
    )


@app.get("/sensors")
async def get_sensors(request: Request):
    """Get current sensor readings."""
    temp = 20 + np.random.uniform(-2, 2)
    humidity = 45 + np.random.uniform(-5, 5)
    motion = "🚶 Detected" if np.random.random() < 0.2 else "✅ Clear"

    return templates.TemplateResponse(
        "sensors.html",
        {
            "request": request,
            "temperature": f"{temp:.1f}°C",
            "humidity": f"{humidity:.1f}%",
            "motion": motion,
        }
    )


@app.get("/devices")
async def get_devices(request: Request):
    """Get device status."""
    devices = [
        ("Living Room Light", state["living_room_light"]),
        ("Bedroom Light", state["bedroom_light"]),
        ("Kitchen Light", state["kitchen_light"]),
        ("Camera", state["camera_enabled"]),
        ("Temperature Sensor", True),
        ("Motion Detector", True),
    ]

    return templates.TemplateResponse(
        "devices.html",
        {
            "request": request,
            "devices": devices,
            "last_update": datetime.now().strftime('%H:%M:%S')
        }
    )


if __name__ == "__main__":
    print("Starting FastAPI + HTMX IoT Dashboard on http://localhost:8000")
    uvicorn.run(app, host="0.0.0.0", port=8000)

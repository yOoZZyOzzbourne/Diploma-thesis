# Dash IoT Demo

IoT control system for BroadbandLIGHT thesis.

## Run

```bash
./start.sh
```

Open: http://localhost:8050

## What's Inside

**Dashboard** - Overview, metrics, charts
**Light Control** - 3 lights with power, brightness, color temp
**Parking Lot** - 6 spots with occupancy map
**Sensors** - Temp, humidity, light gauges + charts
**Cameras** - 2 cameras with controls
**Logs** - Device action history

## Tech Stack

- `dash` - Framework
- `dash-daq` - IoT widgets (gauges, sliders, LEDs)
- `dash-bootstrap-components` - UI
- `paho-mqtt` - MQTT (mocked)
- `sqlalchemy` - Database

## Files

- `app_iot.py` - Main app
- `mock_mqtt.py` - Fake MQTT
- `database.py` - SQLite models
- `DOCUMENTATION.md` - Full docs

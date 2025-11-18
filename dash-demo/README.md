# BroadbandLIGHT IoT Control System - Dash Demo

Professional IoT control and monitoring system built with Dash, demonstrating capabilities for your thesis.

## Features

### 6 Tabs with Full Functionality

**1. Dashboard**
- Real-time system status
- Active lights counter
- Parking occupancy overview
- Live temperature monitoring
- Real-time sensor charts (temperature, humidity, light level)
- Quick controls for all lights

**2. Light Control**
- 3 independent light fixtures with full control
- Power on/off with visual indicators (DAQ PowerButton + Indicator)
- Brightness control (0-100%) with live sliders
- Color temperature control (2700K-6500K) - Warm to Cool
- Real-time status display
- MQTT command publishing
- Database logging of all actions

**3. Parking Lot**
- Visual parking map (6 spots)
- Color-coded occupancy (green = free, red = occupied)
- Real-time statistics
- Duration tracking for occupied spots
- Occupancy rate calculation

**4. Sensors**
- Live gauge displays for:
  - Temperature (0-50°C)
  - Humidity (0-100%)
  - Light level (0-1000 lux)
  - Motion detection indicator
- Historical sensor data charts
- Auto-refresh every 2 seconds

**5. Cameras**
- 2 camera feeds with controls
- Power on/off switches
- Recording toggle
- Live feed placeholders

**6. Logs**
- Complete device control history
- Filterable and sortable table
- Timestamp tracking
- Database-backed persistence

## Technologies Used

**Core:**
- `dash` - Web framework
- `dash-bootstrap-components` - Professional UI components
- `dash-daq` - IoT control widgets (gauges, sliders, indicators)
- `plotly` - Interactive charts

**IoT Integration:**
- `paho-mqtt` - MQTT client (mocked for demo)
- `sqlalchemy` - Database ORM
- SQLite database for logging

## Architecture

```
dash-demo/
├── app_iot.py          # Main IoT application
├── app.py              # Analytics dashboard (original)
├── mock_mqtt.py        # Mock MQTT client
├── database.py         # SQLAlchemy models
├── iot_system.db       # SQLite database (auto-created)
└── requirements.txt    # Dependencies
```

## Running the Demo

```bash
./start.sh
```

Access at: http://localhost:8050

## Key Components Demonstrated

**DAQ Components:**
- `daq.PowerButton` - Light power controls
- `daq.Indicator` - Status LEDs
- `daq.Slider` - Brightness & color temperature
- `daq.Gauge` - Sensor readings
- `daq.BooleanSwitch` - Camera controls

**Real-time Updates:**
- Interval components for auto-refresh
- Multiple update frequencies (2s, 3s, 30s)
- Callback-based state management

**Database Integration:**
- Sensor readings logged to database
- Device actions tracked
- Historical data queries

**MQTT Simulation:**
- Publish commands to devices
- Device state management
- Topic-based routing

## Perfect for Thesis Because:

1. **Modular Design** - Easy to add new devices
2. **Professional Components** - Production-ready UI
3. **Real IoT Patterns** - MQTT, database, real-time updates
4. **Well Documented** - Clear code structure
5. **Extensible** - Simple to connect real hardware
6. **Industry Standard** - Used in real IoT deployments

## Next Steps for Real Implementation

1. Replace `mock_mqtt.py` with real MQTT broker connection
2. Connect actual sensors to MQTT topics
3. Add authentication/authorization
4. Deploy with production WSGI server (Gunicorn)
5. Add SSL/TLS for security
6. Implement data retention policies
7. Add alerting/notification system

# Smart Parking Lot Control System

Modern web-based control interface for the BroadbandLIGHT smart parking lot at VŠB-TUO using Dash framework.

## Features

- **Real-time MQTT Control** - Direct connection to parking lot MQTT broker (158.196.15.41)
- **Light Control** - Control 18 lights across 10 poles individually or all at once
- **Beacon Control** - Manage 3 warning beacons (majáčky)
- **Dashboard** - Overview and quick controls
- **Weather Station** - Integration ready for GIOM 3000 meteostanice
- **Camera Views** - Display for 4 security cameras
- **Modern UI** - Responsive dark theme interface with Bootstrap

## System Architecture

```
parking-lot-dash/
├── src/
│   ├── app.py              # Main Dash application
│   └── mqtt_client.py      # MQTT communication handler
├── config/
│   └── devices.py          # Parking lot device configuration
├── scripts/
│   ├── setup.sh            # Setup script
│   ├── start.sh            # Start application
│   └── deploy.sh           # Deploy to remote server
├── requirements.txt        # Python dependencies
├── .env.example           # Environment variables template
└── README.md              # This file
```

## Device Configuration

Based on thesis Table 2.1:

- **10 Light Poles** - 18 lights total (BOOS Naica, Thorn R2L2, Schreder Teceo, L2LED L2CB)
- **3 Beacons** - Warning beacons on poles 4, 5, and 7
- **4 Cameras** - AXIS P1435-LE and DAHUA IPC-HDBW1220E
- **Weather Station** - GIOM 3000 on pole 2

## Quick Start

### Local Installation

```bash
# 1. Navigate to project directory
cd parking-lot-dash

# 2. Run setup
./scripts/setup.sh

# 3. Configure environment
cp .env.example .env
nano .env  # Edit MQTT settings if needed

# 4. Start application
./scripts/start.sh
```

Access at: **http://localhost:8050**

### Remote Deployment

Deploy to the parking lot server:

```bash
# Deploy to parkoviste@158.196.15.41
./scripts/deploy.sh
```

Then on the remote server:

```bash
# SSH to server
ssh parkoviste@158.196.15.41

# Navigate to app
cd ../fic0027/parking-lot-dash

# Edit configuration
nano .env

# Start application
./scripts/start.sh
```

## Configuration

### Environment Variables (.env)

```bash
# MQTT Broker Configuration
MQTT_BROKER=158.196.15.41
MQTT_PORT=1883
MQTT_KEEPALIVE=60

# Application Configuration
DASH_HOST=0.0.0.0
DASH_PORT=8050
DASH_DEBUG=False
```

### MQTT Topics

Based on thesis Table 5.1:

| Purpose | Topic |
|---------|-------|
| Set light power | `lights/device/{mac}/segment/{segment}/power/set` |
| Get light power | `lights/device/{mac}/segment/{segment}/power/get` |
| Light power response | `lights/device/{mac}/segment/{segment}/power` |
| Get telemetry | `lights/device/{mac}/telemetry/get` |
| Telemetry response | `lights/device/{mac}/telemetry/{property}` |
| Discover lights | `lights/discovery/request` |
| Discovery response | `lights/discovery/reply` |

## Usage

### Dashboard Tab
- Overview statistics
- Quick controls for all lights and beacons
- System status indicators
- Current time display

### Osvětlení (Lights) Tab
- Individual control for all 10 poles
- Each pole shows its light types (BOOS, Thorn, Schreder, L2LED)
- Power slider (0-100%)
- Quick buttons: Off, 50%, 100%
- MAC address display for debugging

### Majáčky (Beacons) Tab
- Control 3 beacons on/off
- Location indicators (pole number)
- MAC address display

### Meteostanice (Weather Station) Tab
- Weather data display (implementation ready)
- Connection via Telnet to 10.11.3.100:23

### Kamery (Cameras) Tab
- 4 camera views
- Location information
- Camera model information

## Technical Details

### MQTT Communication

The application uses `paho-mqtt` to communicate with the Eclipse Mosquitto broker. All communication follows the protocol defined in the thesis (Chapter 5.3).

**Light Control:**
- Power values: 0-100%
- Segment 0 = all segments
- Individual segment control available

**Beacon Control:**
- Binary on/off (0% or 100%)
- More reliable than PWM range

### UI Framework

- **Dash** - Python web framework
- **Dash Bootstrap Components** - Responsive layout
- **Dash DAQ** - IoT-specific widgets (sliders, switches, indicators)
- **Plotly** - Data visualization (for future charts)

### Python Requirements

- Python 3.7+
- All dependencies in `requirements.txt`

## Development

### Adding New Features

1. **New Device Types:**
   - Add to `config/devices.py`
   - Create UI component in `src/app.py`
   - Add MQTT topic handling in `src/mqtt_client.py`

2. **New UI Tab:**
   - Create tab content function in `src/app.py`
   - Add tab to main Tabs component
   - Add callbacks for interactivity

3. **Weather Station Integration:**
   - Implement Telnet client in new file
   - Add data parsing for GIOM 3000 format
   - Create callbacks to update UI

### Testing MQTT Connection

```bash
# Test from command line
mosquitto_sub -h 158.196.15.41 -t "lights/#" -v

# Publish test message
mosquitto_pub -h 158.196.15.41 -t "lights/device/0003F40B09B3/segment/0/power/set" -m "50"
```

## Troubleshooting

### MQTT Connection Issues

1. Check broker is running: `systemctl status mosquitto`
2. Check network connectivity: `ping 158.196.15.41`
3. Verify firewall rules allow port 1883
4. Check OpenVPN/BIRD/OSPF tunnels are up

### Application Won't Start

1. Verify Python version: `python3 --version`
2. Check virtual environment: `source venv/bin/activate`
3. Verify dependencies: `pip list`
4. Check logs for errors

### No Response from Devices

1. Verify MQTT connection status (green indicator)
2. Check device MAC addresses in `config/devices.py`
3. Test with mosquitto_pub/sub tools
4. Check server logs: `/var/log/mosquitto/mosquitto.log`

## Related Files

From original thesis implementation:
- Python scripts: `/parkoviste/Lights/`
- Server scripts: `/parkoviste/Lights/Server/`
- Crontab: `/parkoviste/Lights/lights.crontab`

## References

- Thesis: "Řídicí a vizualizační systém komponent chytrého parkoviště"
- Author: Bc. Jaromír Gasior
- Institution: VŠB-TUO, FEI
- MQTT Broker: Eclipse Mosquitto
- Protocol: MQTT v3.1

## License

Educational project for VŠB-TUO

## Contact

For issues related to the parking lot system, contact FEI VŠB-TUO laboratory EB418.

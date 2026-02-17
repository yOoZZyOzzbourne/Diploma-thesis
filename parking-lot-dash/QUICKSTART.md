# Quick Start Guide

## For Local Development

```bash
cd parking-lot-dash
./scripts/setup.sh
./scripts/start.sh
```

Open browser: **http://localhost:8050**

## For Remote Deployment

```bash
# From your local machine
cd parking-lot-dash
./scripts/deploy.sh

# Then SSH to server
ssh parkoviste@158.196.15.41
cd ../fic0027/parking-lot-dash

# Configure
nano .env  # Set MQTT_BROKER=158.196.15.41

# Start
./scripts/start.sh
```

Access at: **http://158.196.15.41:8050**

## Default Credentials

No authentication required (add if needed for production)

## First Time Setup

1. **Check MQTT Broker**
   ```bash
   systemctl status mosquitto
   ```

2. **Test MQTT Connection**
   ```bash
   mosquitto_sub -h 158.196.15.41 -t "lights/#" -v
   ```

3. **Start Application**
   - Green indicator = Connected ✓
   - Red indicator = Disconnected ✗

## Common Issues

**Can't connect to MQTT:**
- Check VPN/network tunnels (OSPF, BIRD, OpenVPN)
- Verify broker IP: `ping 158.196.15.41`

**Port 8050 already in use:**
- Change `DASH_PORT` in `.env`
- Or stop other service: `pkill -f "python.*app.py"`

**Module not found:**
- Activate venv: `source venv/bin/activate`
- Reinstall: `pip install -r requirements.txt`

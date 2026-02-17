# Deployment Checklist

## Pre-Deployment (Local)

- [ ] Project files created
- [ ] All scripts are executable (`chmod +x scripts/*.sh`)
- [ ] `.env.example` configured
- [ ] README and documentation complete

## Deployment Steps

### 1. Deploy Files to Server

```bash
cd /Users/martinficek/GitKraken/Diploma-thesis
./parking-lot-dash/scripts/deploy.sh
```

**Expected output:**
- ✓ Connection successful
- ✓ Remote directory ready
- ✓ Files synced
- ✓ Setup complete on remote server

### 2. SSH to Server

```bash
ssh parkoviste@158.196.15.41
cd ../fic0027/parking-lot-dash
```

### 3. Configure Application

```bash
# Copy and edit environment file
cp .env.example .env
nano .env
```

**Required settings:**
```bash
MQTT_BROKER=158.196.15.41
MQTT_PORT=1883
MQTT_KEEPALIVE=60

DASH_HOST=0.0.0.0
DASH_PORT=8050
DASH_DEBUG=False
```

### 4. Test MQTT Connection

```bash
# Activate virtual environment
source venv/bin/activate

# Run test
python3 scripts/test_mqtt.py
```

**Expected output:**
- ✓ Connection successful!
- ✓ Client is connected
- ✓ Commands sent successfully
- ✓ All tests passed!

### 5. Start Application

**Option A: Manual Start (for testing)**
```bash
./scripts/start.sh
```

**Option B: As Systemd Service (for production)**
```bash
# Copy service file
sudo cp scripts/parking-lot-dash.service /etc/systemd/system/

# Edit paths if needed
sudo nano /etc/systemd/system/parking-lot-dash.service

# Reload systemd
sudo systemctl daemon-reload

# Enable and start service
sudo systemctl enable parking-lot-dash
sudo systemctl start parking-lot-dash

# Check status
sudo systemctl status parking-lot-dash
```

### 6. Verify Application

**Check Web Interface:**
- Open browser: `http://158.196.15.41:8050`
- MQTT status indicator should be green ✓
- All tabs should load correctly

**Check Logs:**
```bash
# If running as service
sudo journalctl -u parking-lot-dash -f

# If running manually
# Check terminal output
```

### 7. Test Controls

- [ ] Dashboard tab loads
- [ ] Lights tab shows all 10 poles
- [ ] Beacons tab shows 3 beacons
- [ ] Weather tab displays
- [ ] Cameras tab displays
- [ ] Light sliders work
- [ ] Quick control buttons work
- [ ] Beacon switches work
- [ ] MQTT status indicator is green

## Post-Deployment

### Integration with Existing System

**Check compatibility with existing scripts:**
```bash
# Existing Python scripts location
ls -la /parkoviste/Lights/

# Verify MQTT broker
systemctl status mosquitto

# Check network tunnels
systemctl status openvpn@*
systemctl status bird
```

### Monitoring

**Watch MQTT traffic:**
```bash
mosquitto_sub -h 158.196.15.41 -t "lights/#" -v
```

**Monitor application logs:**
```bash
# As service
sudo journalctl -u parking-lot-dash -f

# Check mosquitto logs
sudo tail -f /var/log/mosquitto/mosquitto.log
```

### Troubleshooting

**If MQTT won't connect:**
1. Check mosquitto service: `systemctl status mosquitto`
2. Check network: `ping 158.196.15.41`
3. Check firewall: `sudo ufw status`
4. Verify OpenVPN tunnels: `ip addr show | grep tap`

**If web interface won't load:**
1. Check if port is in use: `netstat -tulpn | grep 8050`
2. Check application logs
3. Verify venv is activated
4. Check Python version: `python3 --version`

**If devices don't respond:**
1. Verify MAC addresses in `config/devices.py`
2. Test with mosquitto_pub directly
3. Check server logs: `/var/log/mosquitto/mosquitto.log`
4. Verify device states in MQTT

## Rollback Plan

**If issues occur:**

1. Stop new application:
   ```bash
   sudo systemctl stop parking-lot-dash
   # or
   pkill -f "python.*app.py"
   ```

2. Use existing Node-RED interface:
   ```bash
   # Start Node-RED if needed
   node-red
   ```

3. Access at: `http://158.196.15.41:1880/ui`

## Success Criteria

- [x] Application deployed to server
- [ ] MQTT connection established (green indicator)
- [ ] Can control at least one light
- [ ] Can control at least one beacon
- [ ] All tabs load without errors
- [ ] No conflicts with existing system
- [ ] Logs show no critical errors

## Next Steps

After successful deployment:

1. **Add Authentication** (if needed)
2. **Implement Weather Station** (Telnet to GIOM 3000)
3. **Add Camera Streams** (if cameras support RTSP/HTTP)
4. **Add Historical Data** (charts, logs)
5. **Mobile Responsiveness** (test on tablets/phones)
6. **Backup Strategy** (database, configs)

## Contact

For issues: FEI VŠB-TUO, Laboratory EB418

## Documentation

- Main README: `README.md`
- Quick start: `QUICKSTART.md`
- This checklist: `DEPLOYMENT_CHECKLIST.md`

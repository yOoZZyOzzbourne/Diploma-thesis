# Camera Integration Guide

## Camera Models

From thesis:
1. **AXIS P1435-LE** (Pole 1, Brána) - Gate camera
2. **DAHUA IPC-HDBW1220E** (Pole 3) - Parking area 1
3. **DAHUA IPC-HDBW1220E** (Pole 6) - Parking area 2
4. **DAHUA IPC-HDBW1220E** (Pole 7) - Parking area 3

## Find Camera IPs

### Option 1: Check network
```bash
# Scan network for cameras
nmap -sn 10.11.3.0/24

# Look for HTTP services
nmap -p 80,554,8554 10.11.3.0/24
```

### Option 2: Check router/DHCP
```bash
# On server, check ARP table
arp -a | grep -i "10.11.3"
```

### Option 3: Check documentation
- Look for camera configuration files
- Check thesis Chapter 2.2.1 for IP info

## Common Camera URLs

### AXIS Cameras
```
RTSP: rtsp://[IP]:554/axis-media/media.amp
HTTP: http://[IP]/mjpg/video.mjpg
Snapshot: http://[IP]/axis-cgi/jpg/image.cgi
```

### DAHUA Cameras
```
RTSP Main: rtsp://[IP]:554/cam/realmonitor?channel=1&subtype=0
RTSP Sub: rtsp://[IP]:554/cam/realmonitor?channel=1&subtype=1
Snapshot: http://[IP]/cgi-bin/snapshot.cgi
```

## Add to Dash App

### Step 1: Update config/devices.py

```python
CAMERAS = {
    1: {
        'name': 'AXIS P1435-LE',
        'pole': 1,
        'location': 'Brána',
        'ip': '10.11.3.101',  # ← Add actual IP
        'rtsp': 'rtsp://10.11.3.101:554/axis-media/media.amp',
        'snapshot': 'http://10.11.3.101/axis-cgi/jpg/image.cgi'
    },
    2: {
        'name': 'DAHUA IPC-HDBW1220E',
        'pole': 3,
        'location': 'Parkoviště 1',
        'ip': '10.11.3.102',  # ← Add actual IP
        'rtsp': 'rtsp://10.11.3.102:554/cam/realmonitor?channel=1&subtype=0',
        'snapshot': 'http://10.11.3.102/cgi-bin/snapshot.cgi'
    },
    # ... etc
}
```

### Step 2: Add snapshot endpoint to app.py

Add this to `src/app.py`:

```python
import requests
from flask import Response
import base64

# Add this route
@app.server.route('/camera/<int:camera_id>/snapshot')
def camera_snapshot(camera_id):
    """Proxy camera snapshot to avoid CORS issues"""
    camera = CAMERAS.get(camera_id)
    if not camera:
        return "Camera not found", 404

    try:
        # Fetch snapshot from camera
        response = requests.get(
            camera['snapshot'],
            timeout=5,
            auth=('admin', 'password')  # Add camera credentials
        )
        return Response(response.content, mimetype='image/jpeg')
    except Exception as e:
        return f"Error: {e}", 500
```

### Step 3: Update camera display

Replace camera placeholder in `create_cameras_tab()`:

```python
def create_cameras_tab():
    """Create cameras view tab"""
    camera_cards = []
    for cam_id, cam_data in CAMERAS.items():
        camera_cards.append(
            dbc.Col([
                dbc.Card([
                    dbc.CardHeader([
                        html.I(className="fas fa-video me-2"),
                        cam_data['name']
                    ]),
                    dbc.CardBody([
                        # Live snapshot with auto-refresh
                        html.Img(
                            id={'type': 'camera-img', 'id': cam_id},
                            src=f'/camera/{cam_id}/snapshot',
                            style={'width': '100%', 'height': 'auto'},
                            className='rounded'
                        ),
                        html.Div([
                            html.P([
                                html.I(className="fas fa-map-marker-alt me-2"),
                                cam_data['location']
                            ], className="mb-1"),
                            html.P([
                                html.I(className="fas fa-network-wired me-2"),
                                cam_data.get('ip', 'N/A')
                            ], className="mb-0 text-muted")
                        ], className="mt-3")
                    ])
                ])
            ], width=12, md=6, lg=3, className="mb-3")
        )

    return dbc.Container([
        html.H3("Kamery", className="mb-3"),
        dbc.Row(camera_cards),
        dcc.Interval(id='camera-refresh', interval=5000, n_intervals=0)  # Refresh every 5s
    ], fluid=True)

# Add callback to refresh images
@app.callback(
    Output({'type': 'camera-img', 'id': ALL}, 'src'),
    Input('camera-refresh', 'n_intervals')
)
def refresh_cameras(n):
    """Refresh camera images"""
    return [f'/camera/{cam_id}/snapshot?t={n}' for cam_id in CAMERAS.keys()]
```

## For RTSP Streaming (Advanced)

If you want live video instead of snapshots:

### Option 1: Use VLC Web Plugin
```html
<embed type="application/x-vlc-plugin"
       target="rtsp://[IP]:554/cam/realmonitor?channel=1&subtype=0"
       width="640" height="480" />
```

### Option 2: Convert RTSP to HLS with ffmpeg
```bash
# Install ffmpeg
apt install ffmpeg

# Stream camera to HLS
ffmpeg -rtsp_transport tcp -i rtsp://[IP]:554/... \
    -c:v copy -c:a aac -f hls -hls_time 2 -hls_list_size 3 \
    /var/www/html/camera1/stream.m3u8
```

Then use video.js player in Dash:
```python
html.Video(
    src='/camera1/stream.m3u8',
    controls=True,
    autoPlay=True,
    style={'width': '100%'}
)
```

## Security

Add camera credentials to `.env`:

```bash
# Camera Credentials
CAMERA_USERNAME=admin
CAMERA_PASSWORD=your_password
```

Use in code:
```python
import os
auth = (os.getenv('CAMERA_USERNAME'), os.getenv('CAMERA_PASSWORD'))
```

## Testing

```bash
# Test camera access
curl http://[CAMERA_IP]/axis-cgi/jpg/image.cgi --user admin:password -o test.jpg

# View snapshot
open test.jpg  # macOS
xdg-open test.jpg  # Linux
```

## Troubleshooting

**Can't access camera:**
- Check camera is on network: `ping [CAMERA_IP]`
- Verify credentials
- Check firewall rules

**CORS errors:**
- Use the proxy endpoint (app.server.route)
- Or add CORS headers to camera config

**Slow loading:**
- Use substream instead of mainstream
- Reduce resolution in camera settings
- Increase Interval refresh time

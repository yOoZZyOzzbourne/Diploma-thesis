#!/usr/bin/env python3
"""
Quick camera configuration tool
Updates config/devices.py with camera IPs
"""

print("=" * 50)
print("Camera Configuration Tool")
print("=" * 50)
print()

print("Discovered cameras from network scan:")
print()
print("Enter camera IPs (or press Enter to skip):")
print()

# Camera configuration
cameras = {}

# AXIS camera (Gate)
print("1. AXIS P1435-LE (Brána, Pole 1)")
ip = input("   IP address [e.g., 10.11.3.101]: ").strip()
if ip:
    cameras[1] = {
        'ip': ip,
        'snapshot_url': f'http://{ip}/axis-cgi/jpg/image.cgi'
    }
print()

# DAHUA cameras
for i, location in enumerate(["Parkoviště 1 (Pole 3)", "Parkoviště 2 (Pole 6)", "Parkoviště 3 (Pole 7)"], start=2):
    print(f"{i}. DAHUA IPC-HDBW1220E ({location})")
    ip = input(f"   IP address [e.g., 10.11.3.{100+i}]: ").strip()
    if ip:
        cameras[i] = {
            'ip': ip,
            'snapshot_url': f'http://{ip}/cgi-bin/snapshot.cgi'
        }
    print()

if not cameras:
    print("No cameras configured. Exiting.")
    exit(0)

print()
print("=" * 50)
print("Configuration Summary:")
print("=" * 50)
for cam_id, cam_data in cameras.items():
    print(f"Camera {cam_id}: {cam_data['ip']}")
    print(f"  URL: {cam_data['snapshot_url']}")
print()

# Ask for credentials
print("Camera credentials:")
username = input("Username [default: admin]: ").strip() or "admin"
password = input("Password [default: admin]: ").strip() or "admin"
print()

# Generate config
print("=" * 50)
print("Add this to config/devices.py:")
print("=" * 50)
print()

for cam_id, cam_data in cameras.items():
    print(f"    {cam_id}: {{")
    print(f"        'ip': '{cam_data['ip']}',")
    print(f"        'snapshot_url': '{cam_data['snapshot_url']}',")
    print(f"    }},")

print()
print("And update CAMERA_AUTH:")
print(f"CAMERA_AUTH = ('{username}', '{password}')")
print()

# Test cameras
print("=" * 50)
print("Testing cameras...")
print("=" * 50)

import subprocess

for cam_id, cam_data in cameras.items():
    print(f"\nTesting Camera {cam_id} ({cam_data['ip']})...")

    cmd = [
        'curl', '-s', '-m', '5',
        '--user', f'{username}:{password}',
        cam_data['snapshot_url'],
        '-o', f'/tmp/camera_{cam_id}_test.jpg'
    ]

    result = subprocess.run(cmd, capture_output=True)

    if result.returncode == 0:
        print(f"  ✓ Success! Snapshot saved to /tmp/camera_{cam_id}_test.jpg")
        print(f"  View: xdg-open /tmp/camera_{cam_id}_test.jpg")
    else:
        print(f"  ✗ Failed to get snapshot")
        print(f"  Check IP, URL, and credentials")

print()
print("=" * 50)
print("Next steps:")
print("1. Update config/devices.py with the IPs above")
print("2. Restart the application")
print("3. Check 'Kamery' tab in the web interface")
print("=" * 50)

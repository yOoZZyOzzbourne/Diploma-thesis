#!/usr/bin/env python3
"""
Test different camera snapshot URLs to find the correct one
"""
import requests
from requests.auth import HTTPBasicAuth

# Camera details
camera_ip = "158.196.246.48"
username = "root"
password = "Student123?"

# Common snapshot URL patterns to try
url_patterns = [
    # AXIS cameras
    "/axis-cgi/jpg/image.cgi",
    "/aca/axis-cgi/jpg/image.cgi",

    # Generic snapshot endpoints
    "/snapshot.jpg",
    "/aca/snapshot.jpg",
    "/image.jpg",
    "/aca/image.jpg",
    "/jpg/image.jpg",
    "/aca/jpg/image.jpg",

    # CGI endpoints
    "/cgi-bin/snapshot.cgi",
    "/aca/cgi-bin/snapshot.cgi",
    "/cgi-bin/image.cgi",
    "/aca/cgi-bin/image.cgi",

    # Video/Stream endpoints
    "/video.cgi",
    "/aca/video.cgi",
    "/videostream.cgi",
    "/aca/videostream.cgi",
    "/mjpg/video.cgi",
    "/aca/mjpg/video.cgi",

    # Other common patterns
    "/img/snapshot.cgi",
    "/aca/img/snapshot.cgi",
    "/tmpfs/auto.jpg",
    "/aca/tmpfs/auto.jpg",
    "/snap.jpg",
    "/aca/snap.jpg",
]

print("=" * 70)
print("Camera Snapshot URL Tester")
print("=" * 70)
print(f"\nTesting camera at: {camera_ip}")
print(f"Username: {username}")
print(f"Base URL: http://{camera_ip}/aca/")
print("\nTrying different snapshot URLs...\n")
print("-" * 70)

successful_urls = []

for pattern in url_patterns:
    url = f"http://{camera_ip}{pattern}"
    try:
        response = requests.get(
            url,
            auth=HTTPBasicAuth(username, password),
            timeout=3,
            verify=False
        )

        status = response.status_code
        content_type = response.headers.get('Content-Type', 'unknown')
        size = len(response.content)

        if status == 200:
            if 'image' in content_type or size > 1000:  # Likely an image
                print(f"✓ SUCCESS: {pattern}")
                print(f"  Status: {status}")
                print(f"  Content-Type: {content_type}")
                print(f"  Size: {size} bytes")
                print()
                successful_urls.append((pattern, content_type, size))
            else:
                print(f"? FOUND: {pattern} (but might not be an image)")
                print(f"  Status: {status}, Type: {content_type}, Size: {size}")
                print()
        elif status == 401:
            print(f"✗ DENIED: {pattern} - Authentication failed (401)")
        elif status == 404:
            print(f"  SKIP: {pattern} - Not found (404)")
        else:
            print(f"? OTHER: {pattern} - Status {status}")

    except requests.exceptions.Timeout:
        print(f"  TIMEOUT: {pattern}")
    except requests.exceptions.ConnectionError:
        print(f"  ERROR: {pattern} - Connection error")
    except Exception as e:
        print(f"  ERROR: {pattern} - {str(e)}")

print("-" * 70)
print("\nSUMMARY:")
print("=" * 70)

if successful_urls:
    print(f"\n✓ Found {len(successful_urls)} working URL(s):\n")
    for url, content_type, size in successful_urls:
        print(f"  • {url}")
        print(f"    Type: {content_type}, Size: {size} bytes")
        print()

    print("RECOMMENDED URL:")
    print(f"  http://{camera_ip}{successful_urls[0][0]}")
else:
    print("\n✗ No working snapshot URLs found.")
    print("\nNext steps:")
    print("1. Open http://158.196.246.48/aca/index.html in your browser")
    print("2. Open Developer Tools (F12) -> Network tab")
    print("3. Look for image requests (JPEG/JPG files)")
    print("4. Share the URL of the image request")

print("\n" + "=" * 70)

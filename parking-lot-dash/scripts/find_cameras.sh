#!/bin/bash
# Quick script to find cameras on network

echo "==================================="
echo "Camera Discovery Tool"
echo "==================================="
echo ""

# Check if nmap is installed
if ! command -v nmap &> /dev/null; then
    echo "Installing nmap..."
    sudo apt-get update && sudo apt-get install -y nmap
fi

echo "Scanning network 10.11.3.0/24 for cameras..."
echo ""

# Scan for devices
echo "Active hosts:"
nmap -sn 10.11.3.0/24 | grep "Nmap scan report"
echo ""

# Scan for HTTP/RTSP ports (cameras usually have these)
echo "Scanning for camera services (HTTP/RTSP)..."
nmap -p 80,554,8000,8080 10.11.3.0/24 | grep -E "Nmap scan report|80/tcp|554/tcp|8000/tcp|8080/tcp"
echo ""

echo "==================================="
echo "Testing common camera IPs..."
echo "==================================="
echo ""

# Common camera IPs to test
COMMON_IPS=("10.11.3.101" "10.11.3.102" "10.11.3.103" "10.11.3.104" "10.11.3.10" "10.11.3.11" "10.11.3.12" "10.11.3.13")

for IP in "${COMMON_IPS[@]}"; do
    echo -n "Testing $IP ... "

    # Try ping first
    if ping -c 1 -W 1 $IP &> /dev/null; then
        echo -n "✓ Online "

        # Try AXIS snapshot
        if curl -s -m 2 "http://$IP/axis-cgi/jpg/image.cgi" --user admin:admin -o /tmp/test_${IP}.jpg 2>/dev/null; then
            echo "→ AXIS camera found! Snapshot saved to /tmp/test_${IP}.jpg"
            echo "   URL: http://$IP/axis-cgi/jpg/image.cgi"
        # Try DAHUA snapshot
        elif curl -s -m 2 "http://$IP/cgi-bin/snapshot.cgi" --user admin:admin -o /tmp/test_${IP}.jpg 2>/dev/null; then
            echo "→ DAHUA camera found! Snapshot saved to /tmp/test_${IP}.jpg"
            echo "   URL: http://$IP/cgi-bin/snapshot.cgi"
        else
            echo "→ Device found but not recognized as camera"
        fi
    else
        echo "✗ Offline"
    fi
done

echo ""
echo "==================================="
echo "Check /tmp/ for saved snapshots:"
echo "ls -lh /tmp/test_*.jpg"
echo ""
echo "View snapshot: xdg-open /tmp/test_[IP].jpg"
echo "==================================="

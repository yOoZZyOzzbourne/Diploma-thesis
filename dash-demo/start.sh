#!/bin/bash
echo "Starting BroadbandLIGHT IoT Control System..."
echo "Installing dependencies..."
pip install -q -r requirements.txt
echo "Launching app on http://localhost:8050"
echo ""
echo "Available demos:"
echo "  - IoT Control System (recommended): python app_iot.py"
echo "  - Analytics Dashboard: python app.py"
echo ""
python app_iot.py

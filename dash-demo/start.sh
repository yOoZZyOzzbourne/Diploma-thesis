#!/bin/bash
echo "Starting Dash IoT Dashboard..."
echo "Installing dependencies..."
pip install -q -r requirements.txt
echo "Launching app on http://localhost:8050"
python app.py

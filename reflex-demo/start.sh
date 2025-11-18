#!/bin/bash
echo "Starting Reflex IoT Dashboard..."
echo "Installing dependencies..."
pip install -q -r requirements.txt
echo "Initializing Reflex (first run only)..."
reflex init --loglevel warning 2>/dev/null || true
echo "Launching app on http://localhost:3000"
reflex run --loglevel warning

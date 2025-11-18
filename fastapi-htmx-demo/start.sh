#!/bin/bash
echo "Starting FastAPI + HTMX IoT Dashboard..."
echo "Installing dependencies..."
pip install -q -r requirements.txt
echo "Launching app on http://localhost:8000"
python app.py

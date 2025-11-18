#!/bin/bash
echo "Starting Gradio IoT Dashboard..."
echo "Installing dependencies..."
pip install -q -r requirements.txt
echo "Launching app on http://localhost:7860"
python app.py

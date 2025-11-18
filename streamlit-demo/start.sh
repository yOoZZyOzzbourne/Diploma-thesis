#!/bin/bash
echo "Starting Streamlit IoT Dashboard..."
echo "Installing dependencies..."
pip install -q -r requirements.txt
echo "Launching app on http://localhost:8501"
streamlit run app.py

#!/bin/bash
# Start script for Parking Lot Dash application

echo "Starting Parking Lot Dash..."
echo ""

# Activate virtual environment
if [ ! -d "venv" ]; then
    echo "Error: Virtual environment not found"
    echo "Please run: ./scripts/setup.sh first"
    exit 1
fi

source venv/bin/activate

# Check if .env exists
if [ ! -f ".env" ]; then
    echo "Warning: .env file not found, using defaults"
fi

# Start the application
echo "Starting application..."
python3 src/app.py

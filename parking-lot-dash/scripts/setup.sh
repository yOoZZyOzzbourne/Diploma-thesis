#!/bin/bash
# Setup script for Parking Lot Dash application

echo "==================================="
echo "Parking Lot Dash - Setup"
echo "==================================="
echo ""

# Check Python version
echo "Checking Python version..."
python3 --version
if [ $? -ne 0 ]; then
    echo "Error: Python 3 is required but not found"
    exit 1
fi
echo ""

# Create virtual environment
echo "Creating virtual environment..."
python3 -m venv venv
if [ $? -ne 0 ]; then
    echo "Error: Failed to create virtual environment"
    exit 1
fi
echo "✓ Virtual environment created"
echo ""

# Activate virtual environment
echo "Activating virtual environment..."
source venv/bin/activate
echo "✓ Virtual environment activated"
echo ""

# Upgrade pip
echo "Upgrading pip..."
pip install --upgrade pip
echo ""

# Install requirements
echo "Installing requirements..."
pip install -r requirements.txt
if [ $? -ne 0 ]; then
    echo "Error: Failed to install requirements"
    exit 1
fi
echo "✓ Requirements installed"
echo ""

# Create .env file if it doesn't exist
if [ ! -f .env ]; then
    echo "Creating .env file from template..."
    cp .env.example .env
    echo "✓ .env file created"
    echo ""
    echo "⚠️  Please edit .env file with your configuration"
else
    echo "✓ .env file already exists"
fi
echo ""

echo "==================================="
echo "Setup complete!"
echo "==================================="
echo ""
echo "Next steps:"
echo "1. Edit .env file with your configuration"
echo "2. Run: ./scripts/start.sh"
echo ""

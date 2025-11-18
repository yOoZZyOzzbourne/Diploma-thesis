#!/bin/bash

echo "=================================="
echo "Starting All Framework Demos"
echo "=================================="
echo ""

# Check if virtual environment exists
if [ ! -d "venv" ]; then
    echo "Error: Virtual environment not found. Please create one first."
    exit 1
fi

# Activate virtual environment
echo "Activating virtual environment..."
source venv/bin/activate

# Install all dependencies
echo ""
echo "Installing dependencies..."
pip install -q streamlit>=1.28.0 pandas>=2.0.0 numpy>=1.24.0 plotly>=5.17.0
pip install -q gradio>=4.0.0
pip install -q dash>=2.14.0

echo ""
echo "=================================="
echo "Starting demos in background..."
echo "=================================="

# Start Streamlit
echo ""
echo "Starting Streamlit demo on http://localhost:8501"
cd streamlit-demo
streamlit run app.py --server.port 8501 > ../streamlit.log 2>&1 &
STREAMLIT_PID=$!
cd ..

# Wait a moment between starts
sleep 2

# Start Gradio
echo "Starting Gradio demo on http://localhost:7860"
cd gradio-demo
python app.py > ../gradio.log 2>&1 &
GRADIO_PID=$!
cd ..

# Wait a moment between starts
sleep 2

# Start Dash
echo "Starting Dash demo on http://localhost:8050"
cd dash-demo
python app.py > ../dash.log 2>&1 &
DASH_PID=$!
cd ..

echo ""
echo "=================================="
echo "All demos started!"
echo "=================================="
echo ""
echo "Access the demos at:"
echo "  - Streamlit: http://localhost:8501"
echo "  - Gradio:    http://localhost:7860"
echo "  - Dash:      http://localhost:8050"
echo ""
echo "Process IDs:"
echo "  - Streamlit PID: $STREAMLIT_PID"
echo "  - Gradio PID:    $GRADIO_PID"
echo "  - Dash PID:      $DASH_PID"
echo ""
echo "Logs are saved to:"
echo "  - streamlit.log"
echo "  - gradio.log"
echo "  - dash.log"
echo ""
echo "To stop all demos, run:"
echo "  kill $STREAMLIT_PID $GRADIO_PID $DASH_PID"
echo ""
echo "Or use: ./stop_all_demos.sh"
echo ""
echo "Saving PIDs to .demo_pids for easy cleanup..."
echo "$STREAMLIT_PID $GRADIO_PID $DASH_PID" > .demo_pids

echo "Press Ctrl+C to stop monitoring. Demos will continue running."
echo ""
echo "Waiting for demos to initialize (checking every 5 seconds)..."
sleep 5

# Check if processes are still running
echo ""
if ps -p $STREAMLIT_PID > /dev/null; then
    echo "✓ Streamlit is running"
else
    echo "✗ Streamlit failed to start (check streamlit.log)"
fi

if ps -p $GRADIO_PID > /dev/null; then
    echo "✓ Gradio is running"
else
    echo "✗ Gradio failed to start (check gradio.log)"
fi

if ps -p $DASH_PID > /dev/null; then
    echo "✓ Dash is running"
else
    echo "✗ Dash failed to start (check dash.log)"
fi

echo ""
echo "All demos are now running in the background!"

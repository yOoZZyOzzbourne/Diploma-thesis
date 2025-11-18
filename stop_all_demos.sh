#!/bin/bash

echo "Stopping all demo processes..."

if [ -f ".demo_pids" ]; then
    PIDS=$(cat .demo_pids)
    echo "Found PIDs: $PIDS"

    for PID in $PIDS; do
        if ps -p $PID > /dev/null 2>&1; then
            echo "Stopping process $PID..."
            kill $PID 2>/dev/null
        else
            echo "Process $PID is not running"
        fi
    done

    rm .demo_pids
    echo "All demos stopped!"
else
    echo "No .demo_pids file found. Trying to find and stop processes by port..."

    # Try to kill by port
    echo "Stopping Streamlit (port 8501)..."
    lsof -ti:8501 | xargs kill -9 2>/dev/null

    echo "Stopping Gradio (port 7860)..."
    lsof -ti:7860 | xargs kill -9 2>/dev/null

    echo "Stopping Dash (port 8050)..."
    lsof -ti:8050 | xargs kill -9 2>/dev/null

    echo "Done!"
fi

# Clean up log files (optional)
read -p "Remove log files? (y/n) " -n 1 -r
echo
if [[ $REPLY =~ ^[Yy]$ ]]; then
    rm -f streamlit.log gradio.log dash.log
    echo "Log files removed."
fi

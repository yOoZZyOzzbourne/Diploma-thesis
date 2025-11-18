# Quick Start Guide

## Setup (One Time)

1. **Create and activate a virtual environment:**
   ```bash
   cd /Users/martinficek/Desktop/DP/iot-demos
   python3 -m venv venv
   source venv/bin/activate
   ```

2. **You're ready!** Each demo will install its own dependencies when you run it.

## Running the Demos

Make sure your venv is activated first:
```bash
source venv/bin/activate
```

Then run any demo:

### Streamlit (Easiest - Try this first!)
```bash
cd streamlit-demo
./start.sh
```
Open: http://localhost:8501

### Gradio
```bash
cd gradio-demo
./start.sh
```
Open: http://localhost:7860

### Dash
```bash
cd dash-demo
./start.sh
```
Open: http://localhost:8050

### Reflex (Takes longer on first run)
```bash
cd reflex-demo
./start.sh
```
Open: http://localhost:3000

### FastAPI + HTMX
```bash
cd fastapi-htmx-demo
./start.sh
```
Open: http://localhost:8000

## Stopping a Demo

Press `Ctrl+C` in the terminal

## When You're Done

```bash
deactivate
```

## Troubleshooting

**Port already in use?**
- Another demo might be running
- Press Ctrl+C to stop it first

**Module not found?**
- Make sure venv is activated: `source venv/bin/activate`
- The start script will install dependencies

**Reflex errors on first run?**
- This is normal - Reflex downloads Node.js dependencies
- Wait for it to complete (can take 1-2 minutes)

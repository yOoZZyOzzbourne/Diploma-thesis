# IoT Dashboard Demos

Comparison of 5 modern Python frameworks for building IoT dashboards with real-time controls and visualizations.

## Overview

Each demo includes:
- 💡 Light switches (Living Room, Bedroom, Kitchen)
- 📊 Real-time sensor data (Temperature, Humidity, Motion)
- 📹 Camera feed toggle
- ⚙️ System status monitoring
- 🔄 Auto-refresh functionality

All demos use **mock data** so you can test them without real IoT devices.

---

## 1. Streamlit

**Best for:** Quick prototypes, data science dashboards, getting started fast

### Features
- Cleanest syntax, minimal code
- Built-in components for all UI elements
- Auto-reload on code changes
- Great for rapid development

### Running
```bash
cd streamlit-demo
./start.sh
```
Opens at: http://localhost:8501

### Pros
- Fastest to build
- Beautiful UI out of the box
- Huge ecosystem and community
- Perfect for data visualization

### Cons
- Less control over HTML/CSS
- Can be slower with very complex apps
- Refresh model (not true real-time WebSocket by default)

---

## 2. Gradio

**Best for:** ML demos, interactive controls, quick interfaces

### Features
- Similar to Streamlit but different focus
- Excellent for input/output interfaces
- Easy to share and deploy
- Built-in theme support

### Running
```bash
cd gradio-demo
./start.sh
```
Opens at: http://localhost:7860

### Pros
- Great for interactive components
- Easy event handling
- Can be embedded in other apps
- Good for ML/AI applications

### Cons
- Slightly less polished than Streamlit for dashboards
- Smaller community than Streamlit
- Limited layout customization

---

## 3. Dash (Plotly)

**Best for:** Enterprise dashboards, complex multi-page apps, production systems

### Features
- Most powerful and flexible
- Excellent for real-time graphs
- Multi-page app support
- Production-ready

### Running
```bash
cd dash-demo
./start.sh
```
Opens at: http://localhost:8050

### Pros
- Best real-time graph updates
- More control than Streamlit
- Great callback system
- Enterprise-grade

### Cons
- More verbose code
- Steeper learning curve
- Requires understanding of callbacks

---

## 4. Reflex

**Best for:** Modern full-stack apps, newest technology, complex state management

### Features
- Pure Python (compiles to React)
- Modern component-based architecture
- Excellent state management
- Very new and actively developed

### Running
```bash
cd reflex-demo
./start.sh
```
Opens at: http://localhost:3000

**Note:** First run will take longer as Reflex initializes and installs Node.js dependencies.

### Pros
- Most modern approach
- Full control like a React app
- Great for complex UIs
- Type-safe and reactive

### Cons
- Youngest framework (less mature)
- Smaller community
- First-time setup takes longer
- Occasional bugs due to newness

---

## 5. FastAPI + HTMX

**Best for:** Production apps, custom requirements, maximum control, RESTful APIs

### Features
- Full control over everything
- Lightweight and fast
- HTMX for reactive UI without heavy JS
- Best performance

### Running
```bash
cd fastapi-htmx-demo
./start.sh
```
Opens at: http://localhost:8000

### Pros
- Maximum flexibility
- Excellent performance
- Can build RESTful API alongside UI
- Modern HTML approach with HTMX

### Cons
- More manual work
- Need to write HTML/CSS
- More code than other options
- Requires web dev knowledge

---

## Quick Comparison

| Framework | Difficulty | Speed | Flexibility | Best For |
|-----------|-----------|-------|-------------|----------|
| **Streamlit** | ⭐ Easy | ⚡⚡⚡ Fast | ⚙️⚙️ Medium | Quick dashboards, prototypes |
| **Gradio** | ⭐ Easy | ⚡⚡⚡ Fast | ⚙️⚙️ Medium | ML demos, interactive tools |
| **Dash** | ⭐⭐ Medium | ⚡⚡ Medium | ⚙️⚙️⚙️ High | Enterprise dashboards |
| **Reflex** | ⭐⭐ Medium | ⚡⚡ Medium | ⚙️⚙️⚙️⚙️ Very High | Modern full-stack apps |
| **FastAPI + HTMX** | ⭐⭐⭐ Hard | ⚡⚡⚡⚡ Very Fast | ⚙️⚙️⚙️⚙️⚙️ Maximum | Production, custom needs |

---

## My Recommendation

**For your IoT dashboard project:**

1. **Start with Streamlit** if you want to:
   - Get something working in 30 minutes
   - Focus on functionality over custom design
   - Iterate quickly

2. **Choose Dash** if you need:
   - Real-time graphs with lots of data
   - Multi-page dashboard
   - Production-ready from day one

3. **Pick Reflex** if you:
   - Want the newest tech
   - Need complex state management
   - Like component-based architecture

4. **Go with FastAPI + HTMX** if you:
   - Need REST APIs for mobile apps too
   - Want maximum performance
   - Have web development experience

---

## Connecting Real IoT Devices

All demos use mock data. To connect real devices:

### MQTT Devices (most common for IoT)
```python
# Add paho-mqtt to requirements.txt
import paho.mqtt.client as mqtt

def on_message(client, userdata, msg):
    # Update your state/data here
    temperature = float(msg.payload)
```

### HTTP/REST APIs
```python
import requests
response = requests.get("http://your-device-ip/sensor")
data = response.json()
```

### Local Hardware (Raspberry Pi GPIO, Arduino)
```python
# For Raspberry Pi
import RPi.GPIO as GPIO

# For Arduino/Serial
import serial
ser = serial.Serial('/dev/ttyUSB0', 9600)
```

---

## License

All demos are free to use, modify, and deploy. No restrictions.

## Questions?

Try each one and see which feels best for your workflow. They're all excellent choices!

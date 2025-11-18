import streamlit as st
import pandas as pd
import numpy as np
from datetime import datetime
import time

# Page config
st.set_page_config(page_title="IoT Dashboard - Streamlit", layout="wide")

# Initialize session state for switches
if 'living_room_light' not in st.session_state:
    st.session_state.living_room_light = False
if 'bedroom_light' not in st.session_state:
    st.session_state.bedroom_light = False
if 'kitchen_light' not in st.session_state:
    st.session_state.kitchen_light = False
if 'camera_enabled' not in st.session_state:
    st.session_state.camera_enabled = True

st.title("🏠 IoT Home Dashboard")
st.markdown("---")

# Main layout
col1, col2 = st.columns([2, 1])

with col1:
    st.header("💡 Light Controls")

    # Light switches in a grid
    switch_col1, switch_col2, switch_col3 = st.columns(3)

    with switch_col1:
        st.session_state.living_room_light = st.toggle(
            "Living Room",
            value=st.session_state.living_room_light,
            key="lr_light"
        )
        if st.session_state.living_room_light:
            st.success("ON")
        else:
            st.error("OFF")

    with switch_col2:
        st.session_state.bedroom_light = st.toggle(
            "Bedroom",
            value=st.session_state.bedroom_light,
            key="br_light"
        )
        if st.session_state.bedroom_light:
            st.success("ON")
        else:
            st.error("OFF")

    with switch_col3:
        st.session_state.kitchen_light = st.toggle(
            "Kitchen",
            value=st.session_state.kitchen_light,
            key="kt_light"
        )
        if st.session_state.kitchen_light:
            st.success("ON")
        else:
            st.error("OFF")

    st.markdown("---")

    # Sensor data
    st.header("📊 Sensor Data")

    # Generate mock sensor data
    current_temp = 20 + np.random.uniform(-2, 2)
    current_humidity = 45 + np.random.uniform(-5, 5)
    current_motion = np.random.choice([True, False], p=[0.2, 0.8])

    metric_col1, metric_col2, metric_col3 = st.columns(3)

    with metric_col1:
        st.metric("🌡️ Temperature", f"{current_temp:.1f}°C", f"{np.random.uniform(-1, 1):.1f}°C")

    with metric_col2:
        st.metric("💧 Humidity", f"{current_humidity:.1f}%", f"{np.random.uniform(-2, 2):.1f}%")

    with metric_col3:
        motion_status = "Detected" if current_motion else "Clear"
        st.metric("🚶 Motion", motion_status)

    # Historical data chart
    st.subheader("Temperature History")

    # Generate mock historical data
    times = pd.date_range(end=datetime.now(), periods=50, freq='1min')
    temps = 20 + np.cumsum(np.random.randn(50) * 0.5)

    chart_data = pd.DataFrame({
        'time': times,
        'temperature': temps
    }).set_index('time')

    st.line_chart(chart_data)

with col2:
    st.header("📹 Camera Feed")

    st.session_state.camera_enabled = st.toggle(
        "Enable Camera",
        value=st.session_state.camera_enabled,
        key="cam_toggle"
    )

    if st.session_state.camera_enabled:
        # Mock camera feed (in real scenario, you'd stream actual camera)
        st.info("📷 Camera Active")
        st.image("camera_placeholder.png",
                 caption="Front Door Camera")
    else:
        st.warning("📷 Camera Disabled")

    st.markdown("---")

    st.header("⚙️ System Status")
    st.success("✅ All systems operational")
    st.info(f"🕐 Last update: {datetime.now().strftime('%H:%M:%S')}")

    # Device status
    st.subheader("Connected Devices")
    devices = [
        ("Living Room Light", st.session_state.living_room_light),
        ("Bedroom Light", st.session_state.bedroom_light),
        ("Kitchen Light", st.session_state.kitchen_light),
        ("Camera", st.session_state.camera_enabled),
        ("Temperature Sensor", True),
        ("Motion Detector", True),
    ]

    for device, status in devices:
        st.text(f"{'🟢' if status else '🔴'} {device}")

# Auto-refresh
st.markdown("---")
if st.button("🔄 Refresh Data"):
    st.rerun()

# Auto-refresh every 5 seconds
st.markdown("*Auto-refreshing every 5 seconds...*")
time.sleep(0.1)  # Small delay to prevent too fast updates

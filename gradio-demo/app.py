import gradio as gr
import pandas as pd
import numpy as np
from datetime import datetime, timedelta
import plotly.graph_objects as go

# Mock sensor data generator
def generate_temp_history():
    times = pd.date_range(end=datetime.now(), periods=50, freq='1min')
    temps = 20 + np.cumsum(np.random.randn(50) * 0.5)

    fig = go.Figure()
    fig.add_trace(go.Scatter(x=times, y=temps, mode='lines', name='Temperature',
                             line=dict(color='#ff7f0e', width=2)))
    fig.update_layout(
        title='Temperature History',
        xaxis_title='Time',
        yaxis_title='Temperature (°C)',
        height=300,
        margin=dict(l=50, r=50, t=50, b=50)
    )
    return fig

def get_sensor_data():
    temp = 20 + np.random.uniform(-2, 2)
    humidity = 45 + np.random.uniform(-5, 5)
    motion = "🚶 Detected" if np.random.random() < 0.2 else "✅ Clear"
    return f"{temp:.1f}°C", f"{humidity:.1f}%", motion

def update_dashboard(lr_light, br_light, kt_light, camera):
    # Get sensor data
    temp, humidity, motion = get_sensor_data()

    # Generate temperature chart
    chart = generate_temp_history()

    # Device status
    devices_status = f"""
    ### Connected Devices
    {'🟢' if lr_light else '🔴'} Living Room Light - {'ON' if lr_light else 'OFF'}
    {'🟢' if br_light else '🔴'} Bedroom Light - {'ON' if br_light else 'OFF'}
    {'🟢' if kt_light else '🔴'} Kitchen Light - {'ON' if kt_light else 'OFF'}
    {'🟢' if camera else '🔴'} Camera - {'Active' if camera else 'Disabled'}
    🟢 Temperature Sensor - Active
    🟢 Motion Detector - Active

    **Last Update:** {datetime.now().strftime('%H:%M:%S')}
    """

    camera_status = "📷 Camera Active" if camera else "📷 Camera Disabled"

    return temp, humidity, motion, chart, devices_status, camera_status

# Create the Gradio interface
with gr.Blocks(title="IoT Dashboard - Gradio", theme=gr.themes.Soft()) as demo:
    gr.Markdown("# 🏠 IoT Home Dashboard")
    gr.Markdown("---")

    with gr.Row():
        with gr.Column(scale=2):
            gr.Markdown("## 💡 Light Controls")

            with gr.Row():
                lr_light = gr.Checkbox(label="Living Room Light", value=False)
                br_light = gr.Checkbox(label="Bedroom Light", value=False)
                kt_light = gr.Checkbox(label="Kitchen Light", value=False)

            gr.Markdown("---")
            gr.Markdown("## 📊 Sensor Data")

            with gr.Row():
                temp_display = gr.Textbox(label="🌡️ Temperature", interactive=False)
                humidity_display = gr.Textbox(label="💧 Humidity", interactive=False)
                motion_display = gr.Textbox(label="🚶 Motion", interactive=False)

            gr.Markdown("### Temperature History")
            temp_chart = gr.Plot()

        with gr.Column(scale=1):
            gr.Markdown("## 📹 Camera Feed")
            camera_toggle = gr.Checkbox(label="Enable Camera", value=True)
            camera_status = gr.Textbox(label="Status", interactive=False)
            gr.Markdown("*Camera feed placeholder (mock camera)*")
            gr.HTML("""
                <div style="background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
                            color: white;
                            padding: 100px 20px;
                            text-align: center;
                            border-radius: 10px;
                            font-size: 24px;
                            font-weight: bold;">
                    📷 Mock Camera Feed
                </div>
            """)

            gr.Markdown("---")
            gr.Markdown("## ⚙️ System Status")
            gr.Markdown("✅ All systems operational")

            devices_status = gr.Markdown()

    gr.Markdown("---")
    refresh_btn = gr.Button("🔄 Refresh Data", variant="primary")

    # Event handlers
    inputs = [lr_light, br_light, kt_light, camera_toggle]
    outputs = [temp_display, humidity_display, motion_display, temp_chart,
               devices_status, camera_status]

    # Update on any change
    lr_light.change(update_dashboard, inputs=inputs, outputs=outputs)
    br_light.change(update_dashboard, inputs=inputs, outputs=outputs)
    kt_light.change(update_dashboard, inputs=inputs, outputs=outputs)
    camera_toggle.change(update_dashboard, inputs=inputs, outputs=outputs)
    refresh_btn.click(update_dashboard, inputs=inputs, outputs=outputs)

    # Initial load
    demo.load(update_dashboard, inputs=inputs, outputs=outputs)

if __name__ == "__main__":
    demo.launch(server_name="0.0.0.0", server_port=7860)

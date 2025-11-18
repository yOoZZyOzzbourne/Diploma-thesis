"""IoT Dashboard built with Reflex."""
import reflex as rx
import numpy as np
from datetime import datetime


class State(rx.State):
    """The app state."""

    # Light switches
    living_room_light: bool = False
    bedroom_light: bool = False
    kitchen_light: bool = False
    camera_enabled: bool = True

    # Sensor data
    temperature: float = 20.0
    humidity: float = 45.0
    motion_detected: bool = False

    # Last update time
    last_update: str = ""

    def toggle_living_room(self):
        """Toggle living room light."""
        self.living_room_light = not self.living_room_light

    def toggle_bedroom(self):
        """Toggle bedroom light."""
        self.bedroom_light = not self.bedroom_light

    def toggle_kitchen(self):
        """Toggle kitchen light."""
        self.kitchen_light = not self.kitchen_light

    def toggle_camera(self):
        """Toggle camera."""
        self.camera_enabled = not self.camera_enabled

    def refresh_sensors(self):
        """Refresh sensor data."""
        self.temperature = 20 + np.random.uniform(-2, 2)
        self.humidity = 45 + np.random.uniform(-5, 5)
        self.motion_detected = np.random.random() < 0.2
        self.last_update = datetime.now().strftime('%H:%M:%S')

    @rx.var
    def temp_display(self) -> str:
        """Format temperature for display."""
        return f"{self.temperature:.1f}°C"

    @rx.var
    def humidity_display(self) -> str:
        """Format humidity for display."""
        return f"{self.humidity:.1f}%"

    @rx.var
    def motion_status(self) -> str:
        """Get motion status."""
        return "🚶 Detected" if self.motion_detected else "✅ Clear"


def light_switch(label: str, is_on: rx.Var, toggle_fn) -> rx.Component:
    """Create a light switch component."""
    return rx.box(
        rx.vstack(
            rx.text(label, font_weight="bold", font_size="lg"),
            rx.switch(
                is_checked=is_on,
                on_change=toggle_fn,
                size="3",
            ),
            rx.cond(
                is_on,
                rx.badge("ON", color_scheme="green", font_size="sm"),
                rx.badge("OFF", color_scheme="red", font_size="sm"),
            ),
            spacing="2",
            align_items="center",
        ),
        padding="4",
        border_radius="lg",
        border="1px solid #e2e8f0",
        bg="white",
    )


def metric_card(icon: str, label: str, value: str) -> rx.Component:
    """Create a metric card component."""
    return rx.box(
        rx.vstack(
            rx.heading(icon + " " + label, size="5"),
            rx.text(value, font_size="2xl", font_weight="bold", color="blue.600"),
            spacing="2",
        ),
        padding="4",
        border_radius="lg",
        bg="#e8f4f8",
        border="1px solid #bee3f8",
    )


def device_status_item(name: str, is_on: rx.Var) -> rx.Component:
    """Create a device status item."""
    return rx.hstack(
        rx.cond(
            is_on,
            rx.text("🟢", font_size="lg"),
            rx.text("🔴", font_size="lg"),
        ),
        rx.text(name),
        spacing="2",
    )


def index() -> rx.Component:
    """The main dashboard page."""
    return rx.container(
        rx.vstack(
            # Header
            rx.heading("🏠 IoT Home Dashboard", size="9", mb="4"),
            rx.divider(),

            # Main content
            rx.hstack(
                # Left column
                rx.vstack(
                    # Light controls section
                    rx.heading("💡 Light Controls", size="7", color="#34495e"),
                    rx.hstack(
                        light_switch("Living Room", State.living_room_light, State.toggle_living_room),
                        light_switch("Bedroom", State.bedroom_light, State.toggle_bedroom),
                        light_switch("Kitchen", State.kitchen_light, State.toggle_kitchen),
                        spacing="4",
                    ),

                    rx.divider(my="4"),

                    # Sensor data section
                    rx.heading("📊 Sensor Data", size="7", color="#34495e"),
                    rx.hstack(
                        metric_card("🌡️", "Temperature", State.temp_display),
                        metric_card("💧", "Humidity", State.humidity_display),
                        metric_card("🚶", "Motion", State.motion_status),
                        spacing="4",
                    ),

                    rx.button(
                        "🔄 Refresh Sensors",
                        on_click=State.refresh_sensors,
                        size="3",
                        color_scheme="blue",
                        mt="4",
                    ),

                    spacing="4",
                    width="65%",
                ),

                # Right column
                rx.vstack(
                    # Camera section
                    rx.heading("📹 Camera Feed", size="7", color="#34495e"),
                    rx.switch(
                        is_checked=State.camera_enabled,
                        on_change=State.toggle_camera,
                    ),
                    rx.text("Enable Camera", font_weight="bold"),
                    rx.cond(
                        State.camera_enabled,
                        rx.vstack(
                            rx.badge("📷 Camera Active", color_scheme="green", font_size="md"),
                            rx.box(
                                "📷 Mock Camera Feed",
                                bg="#1f77b4",
                                color="white",
                                padding="100px 20px",
                                text_align="center",
                                border_radius="lg",
                                font_size="24px",
                                font_weight="bold",
                            ),
                        ),
                        rx.badge("📷 Camera Disabled", color_scheme="red", font_size="md"),
                    ),

                    rx.divider(my="4"),

                    # System status
                    rx.heading("⚙️ System Status", size="7", color="#34495e"),
                    rx.badge("✅ All systems operational", color_scheme="green", font_size="md"),
                    rx.text(
                        f"🕐 Last update: {State.last_update}",
                        font_size="sm",
                        color="gray.600",
                    ),

                    rx.heading("Connected Devices", size="5", mt="4"),
                    rx.vstack(
                        device_status_item("Living Room Light", State.living_room_light),
                        device_status_item("Bedroom Light", State.bedroom_light),
                        device_status_item("Kitchen Light", State.kitchen_light),
                        device_status_item("Camera", State.camera_enabled),
                        rx.hstack(rx.text("🟢", font_size="lg"), rx.text("Temperature Sensor"), spacing="2"),
                        rx.hstack(rx.text("🟢", font_size="lg"), rx.text("Motion Detector"), spacing="2"),
                        align_items="start",
                        spacing="2",
                    ),

                    spacing="4",
                    width="35%",
                    padding="4",
                    bg="#f8f9fa",
                    border_radius="lg",
                ),

                spacing="6",
                align_items="start",
            ),

            spacing="4",
            padding="4",
        ),
        max_width="1400px",
    )


# Create the app
app = rx.App()
app.add_page(index, on_load=State.refresh_sensors)

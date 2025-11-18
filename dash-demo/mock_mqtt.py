"""Mock MQTT client for demonstration purposes"""
import random
from datetime import datetime

class MockMQTTClient:
    """Simulates MQTT client for demo without actual broker"""

    def __init__(self):
        self.connected = True
        self.devices = {
            'light_1': {'status': False, 'brightness': 50, 'color_temp': 4000},
            'light_2': {'status': False, 'brightness': 75, 'color_temp': 3000},
            'light_3': {'status': False, 'brightness': 100, 'color_temp': 5000},
            'camera_1': {'status': True, 'recording': False},
            'camera_2': {'status': True, 'recording': False},
            'parking_1': {'occupied': False, 'duration': 0},
            'parking_2': {'occupied': True, 'duration': 45},
            'parking_3': {'occupied': False, 'duration': 0},
            'parking_4': {'occupied': True, 'duration': 120},
            'parking_5': {'occupied': False, 'duration': 0},
            'parking_6': {'occupied': True, 'duration': 30},
        }

    def connect(self, broker, port=1883):
        """Mock connect"""
        self.connected = True
        return True

    def publish(self, topic, payload):
        """Mock publish - simulates sending commands to devices"""
        print(f"[MQTT] Published to {topic}: {payload}")

        # Parse topic to update device state
        parts = topic.split('/')
        if len(parts) >= 3:
            device_id = parts[1]
            command = parts[2]

            if device_id in self.devices:
                if command == 'status':
                    self.devices[device_id]['status'] = payload == 'on'
                elif command == 'brightness':
                    self.devices[device_id]['brightness'] = int(payload)
                elif command == 'color_temp':
                    self.devices[device_id]['color_temp'] = int(payload)
                elif command == 'recording':
                    self.devices[device_id]['recording'] = payload == 'on'

    def get_device_state(self, device_id):
        """Get current device state"""
        return self.devices.get(device_id, {})

    def get_sensor_data(self):
        """Mock sensor readings"""
        return {
            'temperature': round(20 + random.uniform(-3, 3), 1),
            'humidity': round(45 + random.uniform(-10, 10), 1),
            'light_level': round(random.uniform(100, 1000), 0),
            'motion_detected': random.choice([True, False]),
            'timestamp': datetime.now().isoformat()
        }

    def disconnect(self):
        """Mock disconnect"""
        self.connected = False

# Global mock client instance
mqtt_client = MockMQTTClient()

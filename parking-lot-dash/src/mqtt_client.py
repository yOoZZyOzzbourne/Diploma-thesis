"""
MQTT Client for Parking Lot Communication
"""
import paho.mqtt.client as mqtt
import json
import logging
from typing import Callable, Dict, Any
import os
from dotenv import load_dotenv

load_dotenv()

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)


class ParkingLotMQTT:
    """MQTT client for parking lot control and monitoring"""

    def __init__(self):
        self.broker = os.getenv('MQTT_BROKER', '158.196.15.41')
        self.port = int(os.getenv('MQTT_PORT', 1883))
        self.keepalive = int(os.getenv('MQTT_KEEPALIVE', 60))

        self.client = mqtt.Client(client_id="parking_lot_dash")
        self.client.on_connect = self._on_connect
        self.client.on_message = self._on_message
        self.client.on_disconnect = self._on_disconnect

        self.connected = False
        self.message_callbacks: Dict[str, Callable] = {}
        self.device_states: Dict[str, Any] = {}

    def _on_connect(self, client, userdata, flags, rc):
        """Callback when connected to MQTT broker"""
        if rc == 0:
            logger.info(f"Connected to MQTT broker at {self.broker}:{self.port}")
            self.connected = True
            # Subscribe to all light power topics
            client.subscribe("lights/device/+/segment/+/power")
            # Subscribe to telemetry
            client.subscribe("lights/device/+/telemetry/#")
            # Subscribe to discovery
            client.subscribe("lights/discovery/reply")
        else:
            error_messages = {
                1: "Connection refused - incorrect protocol version",
                2: "Connection refused - invalid client identifier",
                3: "Connection refused - server unavailable",
                4: "Connection refused - bad username or password",
                5: "Connection refused - not authorised"
            }
            logger.error(f"Connection failed: {error_messages.get(rc, f'Unknown error {rc}')}")
            self.connected = False

    def _on_disconnect(self, client, userdata, rc):
        """Callback when disconnected from MQTT broker"""
        logger.warning(f"Disconnected from MQTT broker (rc={rc})")
        self.connected = False

    def _on_message(self, client, userdata, msg):
        """Callback when message received"""
        topic = msg.topic
        try:
            # Try to decode as JSON first
            try:
                payload = json.loads(msg.payload.decode())
            except json.JSONDecodeError:
                # If not JSON, use plain string
                payload = msg.payload.decode()

            logger.debug(f"Received: {topic} -> {payload}")

            # Store in device states
            self.device_states[topic] = payload

            # Call registered callbacks
            for pattern, callback in self.message_callbacks.items():
                if self._topic_matches(pattern, topic):
                    callback(topic, payload)

        except Exception as e:
            logger.error(f"Error processing message: {e}")

    def _topic_matches(self, pattern: str, topic: str) -> bool:
        """Check if topic matches pattern with wildcards"""
        pattern_parts = pattern.split('/')
        topic_parts = topic.split('/')

        if len(pattern_parts) != len(topic_parts):
            return False

        for p, t in zip(pattern_parts, topic_parts):
            if p not in ('+', '#', t):
                return False
        return True

    def connect(self):
        """Connect to MQTT broker"""
        try:
            logger.info(f"Connecting to MQTT broker at {self.broker}:{self.port}")
            self.client.connect(self.broker, self.port, self.keepalive)
            self.client.loop_start()
            return True
        except Exception as e:
            logger.error(f"Failed to connect: {e}")
            return False

    def disconnect(self):
        """Disconnect from MQTT broker"""
        self.client.loop_stop()
        self.client.disconnect()
        self.connected = False
        logger.info("Disconnected from MQTT broker")

    def publish(self, topic: str, payload: Any, qos: int = 0):
        """Publish message to MQTT broker"""
        if not self.connected:
            logger.warning("Not connected to broker, cannot publish")
            return False

        try:
            if isinstance(payload, (dict, list)):
                payload = json.dumps(payload)
            elif not isinstance(payload, str):
                payload = str(payload)

            result = self.client.publish(topic, payload, qos)
            logger.info(f"Published: {topic} -> {payload}")
            return result.rc == mqtt.MQTT_ERR_SUCCESS
        except Exception as e:
            logger.error(f"Publish error: {e}")
            return False

    def subscribe(self, topic: str, callback: Callable = None):
        """Subscribe to topic with optional callback"""
        self.client.subscribe(topic)
        if callback:
            self.message_callbacks[topic] = callback
        logger.info(f"Subscribed to: {topic}")

    def set_light_power(self, mac: str, segment: int, power: float):
        """Set light power (0-100%)"""
        topic = f"lights/device/{mac}/segment/{segment}/power/set"
        self.publish(topic, str(power))

    def get_light_power(self, mac: str, segment: int):
        """Request light power status"""
        topic = f"lights/device/{mac}/segment/{segment}/power/get"
        self.publish(topic, "")

    def set_beacon(self, mac: str, state: bool):
        """Turn beacon on/off"""
        power = 100.0 if state else 0.0
        topic = f"lights/device/{mac}/segment/0/power/set"
        self.publish(topic, str(power))

    def discover_lights(self):
        """Request discovery of all lights"""
        self.publish("lights/discovery/request", "")

    def get_telemetry(self, mac: str, property: str = None):
        """Get device telemetry"""
        if property:
            topic = f"lights/device/{mac}/telemetry/{property}/get"
        else:
            topic = f"lights/device/{mac}/telemetry/get"
        self.publish(topic, "")

    def get_device_state(self, mac: str, segment: int = None) -> Any:
        """Get cached device state"""
        if segment is not None:
            topic = f"lights/device/{mac}/segment/{segment}/power"
        else:
            topic = f"lights/device/{mac}/telemetry"
        return self.device_states.get(topic)

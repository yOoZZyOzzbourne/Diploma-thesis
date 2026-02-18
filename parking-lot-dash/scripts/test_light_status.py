#!/usr/bin/env python3
"""
Test MQTT light status retrieval
"""
import sys
import os

# Add parent directory to path
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from src.mqtt_client import ParkingLotMQTT
from config.devices import LIGHTS
import time

def test_light_status():
    """Test retrieving light status via MQTT"""
    print("=" * 60)
    print("MQTT Light Status Test")
    print("=" * 60)
    print()

    client = ParkingLotMQTT(client_id="parking_lot_test")

    print(f"Broker: {client.broker}:{client.port}")
    print("Connecting...")
    print()

    if not client.connect():
        print("✗ Connection failed!")
        return False

    # Wait for connection to establish
    time.sleep(2)

    if not client.connected:
        print("✗ Client failed to connect properly")
        return False

    print("✓ Connected to MQTT broker")
    print()

    # Request status for all lights
    print("Requesting status for all lights...")
    print("-" * 60)

    for pole_id, pole_data in LIGHTS.items():
        print(f"\n{pole_data['name']}:")
        for device in pole_data['devices']:
            mac = device['mac']
            segment = device['segment']
            device_type = device['type']

            print(f"  {device_type} (MAC: {mac}, Segment: {segment})")
            print(f"    Requesting status...")

            # Request the power status
            client.get_light_power(mac, segment)

    print()
    print("-" * 60)
    print("Waiting 5 seconds for responses...")
    time.sleep(5)

    print()
    print("=" * 60)
    print("MQTT Messages Received:")
    print("=" * 60)

    if not client.device_states:
        print("✗ No messages received!")
        print()
        print("This could mean:")
        print("  1. The lights are not responding")
        print("  2. The MQTT topics are incorrect")
        print("  3. The lights are offline")
    else:
        print(f"✓ Received {len(client.device_states)} messages:")
        print()

        # Group by device
        power_states = {}
        other_states = {}

        for topic, value in sorted(client.device_states.items()):
            if '/power' in topic and '/power/' not in topic:
                power_states[topic] = value
            else:
                other_states[topic] = value

        if power_states:
            print("Power Status Messages:")
            print("-" * 60)
            for topic, value in power_states.items():
                print(f"  {topic}")
                print(f"    Value: {value}")
                print()

        if other_states:
            print("Other Messages:")
            print("-" * 60)
            for topic, value in other_states.items():
                print(f"  {topic}")
                print(f"    Value: {value}")
                print()

    print("=" * 60)

    client.disconnect()
    print("✓ Disconnected")

    return len(client.device_states) > 0

if __name__ == "__main__":
    success = test_light_status()
    print()
    if success:
        print("✓ Test completed - devices are responding!")
    else:
        print("✗ Test completed - no responses received")
    print()
    sys.exit(0 if success else 1)

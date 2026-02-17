#!/usr/bin/env python3
"""
Test MQTT connection and basic functionality
"""
import sys
import os

# Add parent directory to path
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from src.mqtt_client import ParkingLotMQTT
import time

def test_connection():
    """Test basic MQTT connection"""
    print("=" * 50)
    print("MQTT Connection Test")
    print("=" * 50)
    print()

    client = ParkingLotMQTT()

    print(f"Broker: {client.broker}:{client.port}")
    print("Connecting...")

    if client.connect():
        print("✓ Connection successful!")
        print()

        # Wait for connection to establish
        time.sleep(2)

        if client.connected:
            print("✓ Client is connected")
            print()

            # Test discovery
            print("Sending discovery request...")
            client.discover_lights()
            time.sleep(1)

            # Test light control
            print("Testing light control (Stožár 1, Segment 0)...")
            client.set_light_power('0003F40B09B3', 0, 0)
            time.sleep(1)

            print("✓ Commands sent successfully")
            print()

            print("Device states received:")
            for topic, value in client.device_states.items():
                print(f"  {topic}: {value}")

            client.disconnect()
            print()
            print("✓ Disconnected successfully")
            print()
            print("=" * 50)
            print("All tests passed! ✓")
            print("=" * 50)
            return True
        else:
            print("✗ Client failed to connect properly")
            return False
    else:
        print("✗ Connection failed!")
        print()
        print("Troubleshooting:")
        print("1. Check if MQTT broker is running:")
        print("   systemctl status mosquitto")
        print()
        print("2. Test network connectivity:")
        print(f"   ping {client.broker}")
        print()
        print("3. Check firewall rules:")
        print("   sudo ufw status")
        print()
        print("4. Verify .env configuration")
        return False

if __name__ == "__main__":
    success = test_connection()
    sys.exit(0 if success else 1)

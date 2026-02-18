"""
Weather Station Telnet Client
Connects to GIOM 3000 weather station via Telnet
"""
import socket
import time
import threading
from threading import Lock


class WeatherStationClient:
    def __init__(self, host, port=23, timeout=5):
        self.host = host
        self.port = port
        self.timeout = timeout
        self.lock = Lock()
        self.last_data = {}
        self.connected = False

    def connect_and_read(self):
        """Connect to weather station and read data"""
        with self.lock:
            sock = None
            try:
                print(f"[Weather] Connecting to {self.host}:{self.port}...")

                # Create TCP socket connection
                sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
                sock.settimeout(self.timeout)

                # Connect to weather station
                sock.connect((self.host, self.port))
                print(f"[Weather] Connected successfully!")

                # Wait for menu
                time.sleep(0.5)

                # Receive menu (max 4096 bytes)
                menu = sock.recv(4096).decode('ascii', errors='ignore')
                print(f"[Weather] Received menu ({len(menu)} bytes)")

                # Send "1" to select "Weather information"
                print(f"[Weather] Sending command: 1")
                sock.send(b"1\r\n")

                # Wait for response
                time.sleep(1)

                # Receive weather data
                data = sock.recv(4096).decode('ascii', errors='ignore')

                print(f"[Weather] Received weather data ({len(data)} bytes)")
                print(f"[Weather] Raw data: {repr(data[:500])}")  # Show first 500 chars

                if data:
                    parsed = self.parse_data(data)
                    print(f"[Weather] Parsed data: {parsed}")
                    self.last_data = parsed
                    self.connected = True
                    return self.last_data
                else:
                    print("[Weather] No data received")
                    self.connected = False
                    return {}

            except socket.timeout:
                print(f"[Weather] Connection timeout to {self.host}:{self.port}")
                self.connected = False
                return {}
            except ConnectionRefusedError:
                print(f"[Weather] Connection refused by {self.host}:{self.port}")
                self.connected = False
                return {}
            except Exception as e:
                print(f"[Weather] Connection error: {type(e).__name__}: {e}")
                self.connected = False
                return {}
            finally:
                if sock:
                    try:
                        sock.close()
                    except:
                        pass

    def parse_data(self, raw_data):
        """Parse weather station data"""
        # This is a generic parser - adjust based on actual GIOM 3000 format
        data = {
            'raw': raw_data.strip(),
            'timestamp': time.strftime('%Y-%m-%d %H:%M:%S')
        }

        # Try to parse common weather data patterns
        lines = raw_data.strip().split('\n')

        for line in lines:
            line = line.strip()

            # Temperature (various formats)
            if 'temp' in line.lower() or '°c' in line.lower() or '°C' in line:
                try:
                    # Extract number before °C or after temp
                    parts = line.replace('°C', '').replace('°c', '').split()
                    for part in parts:
                        try:
                            temp = float(part.replace(',', '.'))
                            if -50 < temp < 60:  # Reasonable temperature range
                                data['temperature'] = temp
                                break
                        except ValueError:
                            continue
                except:
                    pass

            # Humidity
            if 'hum' in line.lower() or '%rh' in line.lower():
                try:
                    parts = line.replace('%', '').replace('RH', '').replace('rh', '').split()
                    for part in parts:
                        try:
                            hum = float(part.replace(',', '.'))
                            if 0 <= hum <= 100:
                                data['humidity'] = hum
                                break
                        except ValueError:
                            continue
                except:
                    pass

            # Pressure
            if 'press' in line.lower() or 'hpa' in line.lower() or 'mbar' in line.lower():
                try:
                    parts = line.replace('hPa', '').replace('hpa', '').replace('mbar', '').split()
                    for part in parts:
                        try:
                            press = float(part.replace(',', '.'))
                            if 900 < press < 1100:
                                data['pressure'] = press
                                break
                        except ValueError:
                            continue
                except:
                    pass

            # Wind speed
            if 'wind' in line.lower() or 'm/s' in line.lower() or 'km/h' in line.lower():
                try:
                    parts = line.replace('m/s', '').replace('km/h', '').split()
                    for part in parts:
                        try:
                            wind = float(part.replace(',', '.'))
                            if 0 <= wind < 200:
                                data['wind_speed'] = wind
                                break
                        except ValueError:
                            continue
                except:
                    pass

        return data

    def get_last_data(self):
        return self.last_data

    def start_background_polling(self, interval: int = 60):
        """Poll the weather station in a daemon thread; never blocks Dash callbacks."""
        def _loop():
            while True:
                self.connect_and_read()
                time.sleep(interval)
        t = threading.Thread(target=_loop, daemon=True)
        t.start()

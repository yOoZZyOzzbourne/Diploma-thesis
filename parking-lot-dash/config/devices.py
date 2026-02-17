"""
Parking Lot Device Configuration
Based on Table 2.1 from the thesis
"""

# Light poles (Stožáry) with their MAC addresses and segments
# NOTE: Segments are 1-indexed (devices report segments starting from 1, not 0)
LIGHTS = {
    1: {
        'name': 'Stožár 1',
        'devices': [
            {'mac': '0003F40B09B3', 'segment': 1, 'type': 'BOOS Naica'},
            {'mac': '0003F40B09B3', 'segment': 2, 'type': 'Thorn R2L2'}
        ]
    },
    2: {
        'name': 'Stožár 2',
        'devices': [
            {'mac': '0003F40B089D', 'segment': 1, 'type': 'BOOS Naica'},
            {'mac': '0003F40B089D', 'segment': 2, 'type': 'Thorn R2L2'}
        ]
    },
    3: {
        'name': 'Stožár 3',
        'devices': [
            {'mac': '0003F40B0894', 'segment': 1, 'type': 'BOOS Naica'},
            {'mac': '0003F40B0894', 'segment': 2, 'type': 'Thorn R2L2'}
        ]
    },
    4: {
        'name': 'Stožár 4',
        'devices': [
            {'mac': '0003F40B08C0', 'segment': 1, 'type': 'Thorn R2L2'},
            {'mac': '0003F40B08C0', 'segment': 2, 'type': 'Schreder Teceo'}
        ]
    },
    5: {
        'name': 'Stožár 5',
        'devices': [
            {'mac': '0003F40B0881', 'segment': 1, 'type': 'Thorn R2L2'},
            {'mac': '0003F40B0881', 'segment': 2, 'type': 'Schreder Teceo'}
        ]
    },
    6: {
        'name': 'Stožár 6',
        'devices': [
            {'mac': '0003F409BEDC', 'segment': 1, 'type': 'Thorn R2L2'},
            {'mac': '0003F409BEDC', 'segment': 2, 'type': 'Schreder Teceo'}
        ]
    },
    7: {
        'name': 'Stožár 7',
        'devices': [
            {'mac': '0003f40b088a', 'segment': 1, 'type': 'Schreder Teceo'}
        ]
    },
    8: {
        'name': 'Stožár 8',
        'devices': [
            {'mac': '0003F40B091E', 'segment': 1, 'type': 'Schreder Teceo'}
        ]
    },
    9: {
        'name': 'Stožár 9',
        'devices': [
            {'mac': '0003F40B09AA', 'segment': 1, 'type': 'Schreder Teceo'}
        ]
    },
    10: {
        'name': 'Stožár 10',
        'devices': [
            {'mac': 'deadbeef0001', 'segment': 1, 'type': 'L2LED L2CB'},
            {'mac': 'deadbeef0002', 'segment': 1, 'type': 'L2LED L2CB'}
        ]
    }
}

# Beacons (Majáčky)
BEACONS = {
    1: {'mac': 'B04E2691A611', 'pole': 4, 'name': 'Majáček 1'},
    2: {'mac': 'B04E2691AF51', 'pole': 5, 'name': 'Majáček 2'},
    3: {'mac': 'B04E2691A6AB', 'pole': 7, 'name': 'Majáček 3'}
}

# Cameras
CAMERAS = {
    1: {
        'name': 'AXIS Q1786-LE',
        'pole': 1,
        'location': 'Brána',
        'ip': '158.196.246.48',
        'base_url': 'http://158.196.246.48',
        'snapshot_url': 'http://158.196.246.48/axis-cgi/jpg/image.cgi',
        'stream_url': 'http://158.196.246.48/axis-cgi/mjpg/video.cgi',
        'username': 'root',
        'password': 'Student123?',
        'type': 'axis'
    },
    2: {
        'name': 'DAHUA IPC-HDBW1220E',
        'pole': 3,
        'location': 'Parkoviště 1',
        'ip': None,  # TODO: Přidej IP
        'snapshot_url': None,  # TODO: Přidej URL
        'type': 'dahua'
    },
    3: {
        'name': 'DAHUA IPC-HDBW1220E',
        'pole': 6,
        'location': 'Parkoviště 2',
        'ip': None,  # TODO: Přidej IP
        'snapshot_url': None,  # TODO: Přidej URL
        'type': 'dahua'
    },
    4: {
        'name': 'DAHUA IPC-HDBW1220E',
        'pole': 7,
        'location': 'Parkoviště 3',
        'ip': None,  # TODO: Přidej IP
        'snapshot_url': None,  # TODO: Přidej URL
        'type': 'dahua'
    }
}

# Camera credentials (stored per camera for flexibility)

# Weather Station
WEATHER_STATION = {
    'ip': '10.11.3.100',
    'port': 23,
    'type': 'GIOM 3000',
    'pole': 2
}

# MQTT Topics (from Table 5.1)
MQTT_TOPICS = {
    'discovery_request': 'lights/discovery/request',
    'discovery_reply': 'lights/discovery/reply',
    'light_power_get': 'lights/device/{mac}/segment/{segment}/power/get',
    'light_power_set': 'lights/device/{mac}/segment/{segment}/power/set',
    'light_power': 'lights/device/{mac}/segment/{segment}/power',
    'telemetry_get': 'lights/device/{mac}/telemetry/get',
    'telemetry': 'lights/device/{mac}/telemetry/{property}'
}

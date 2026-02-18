#!/usr/bin/env python3
"""
Dump raw GIOM 3000 telnet output so we can fix the parser.
Run on the server: python scripts/test_weather.py
"""
import sys
import os
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

import socket
import time

HOST = "10.11.3.100"
PORT = 23

def raw_dump():
    sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    sock.settimeout(10)
    print(f"Connecting to {HOST}:{PORT} ...")
    sock.connect((HOST, PORT))
    print("Connected.\n")

    time.sleep(0.5)
    menu = sock.recv(4096).decode("ascii", errors="replace")
    print("=== MENU (raw repr) ===")
    print(repr(menu))
    print("\n=== MENU (plain) ===")
    print(menu)

    print("\nSending '1\\r\\n' ...")
    sock.send(b"1\r\n")
    time.sleep(1.5)

    data = sock.recv(4096).decode("ascii", errors="replace")
    print("\n=== RESPONSE (raw repr) ===")
    print(repr(data))
    print("\n=== RESPONSE (plain) ===")
    print(data)

    sock.close()

    print("\n=== LINE-BY-LINE ===")
    for i, line in enumerate(data.splitlines()):
        print(f"  [{i:02d}] {repr(line)}")

if __name__ == "__main__":
    raw_dump()

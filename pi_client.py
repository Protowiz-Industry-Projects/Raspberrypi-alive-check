#!/usr/bin/env python3
"""
Raspberry Pi Heartbeat Client Script
Sends periodic heartbeat signals to the Raspberry Pi Status Dashboard server.
"""

import requests
import time
import socket
import argparse
import uuid
import psutil

# Default server URL - change this to your server's IP and port
DEFAULT_SERVER_URL = "http://localhost:5000/api/heartbeat"

def get_local_ip():
    """Get the local IP address of this device."""
    try:
        # Connect to a remote server to determine local IP
        s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
        s.connect(("8.8.8.8", 80))
        ip = s.getsockname()[0]
        s.close()
        return ip
    except Exception:
        # Fallback to hostname resolution
        try:
            return socket.gethostbyname(socket.gethostname())
        except Exception:
            return "127.0.0.1"

def get_signal_strength():
    """Simulate getting signal strength. In a real implementation, this would
    depend on your network interface."""
    import random
    strengths = ['Excellent', 'Good', 'Fair', 'Poor']
    return random.choice(strengths)

def send_heartbeat(server_url, device_id, ip_address, signal_strength):
    """Send a heartbeat to the server."""
    payload = {
        "device_id": device_id,
        "ip_address": ip_address,
        "signal_strength": signal_strength
    }
    
    try:
        response = requests.post(server_url, json=payload, timeout=5)
        if response.status_code == 200:
            print(f"[{time.strftime('%Y-%m-%d %H:%M:%S')}] Heartbeat sent successfully")
            return True
        else:
            print(f"[{time.strftime('%Y-%m-%d %H:%M:%S')}] Error: {response.status_code} - {response.text}")
            return False
    except requests.exceptions.RequestException as e:
        print(f"[{time.strftime('%Y-%m-%d %H:%M:%S')}] Failed to send heartbeat: {e}")
        return False

def main():
    parser = argparse.ArgumentParser(description="Raspberry Pi Heartbeat Client")
    parser.add_argument("--server", default=DEFAULT_SERVER_URL, 
                        help="Server URL (default: %(default)s)")
    parser.add_argument("--device-id", default=None, 
                        help="Device ID (default: auto-generated)")
    parser.add_argument("--interval", type=int, default=10,
                        help="Heartbeat interval in seconds (default: %(default)s)")
    
    args = parser.parse_args()
    
    # Generate a device ID if not provided
    if args.device_id is None:
        # Use MAC address as part of the device ID
        mac = ':'.join(['{:02x}'.format((uuid.getnode() >> elements) & 0xff) 
                        for elements in range(0,2*6,2)][::-1])
        device_id = f"pi-{mac.replace(':', '')[-6:]}"
    else:
        device_id = args.device_id
    
    ip_address = get_local_ip()
    
    print(f"Raspberry Pi Heartbeat Client")
    print(f"Server URL: {args.server}")
    print(f"Device ID: {device_id}")
    print(f"IP Address: {ip_address}")
    print(f"Heartbeat Interval: {args.interval} seconds")
    print(f"Press Ctrl+C to stop\n")
    
    try:
        while True:
            signal_strength = get_signal_strength()
            send_heartbeat(args.server, device_id, ip_address, signal_strength)
            time.sleep(args.interval)
    except KeyboardInterrupt:
        print("\nStopping heartbeat client...")

if __name__ == "__main__":
    main()
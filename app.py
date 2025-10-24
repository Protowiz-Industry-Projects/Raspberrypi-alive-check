from flask import Flask, request, jsonify, render_template
import json
import os
from datetime import datetime, timedelta
import threading
import time

app = Flask(__name__)

# File to store device data
DATA_FILE = 'devices.json'

# In-memory storage for devices (in production, you might want to use a proper database)
devices = {}

# Load existing data from file if it exists
if os.path.exists(DATA_FILE):
    try:
        with open(DATA_FILE, 'r') as f:
            devices = json.load(f)
    except:
        devices = {}

# Function to save devices data to file
def save_devices():
    with open(DATA_FILE, 'w') as f:
        json.dump(devices, f, indent=2)

# Background thread to check for offline devices
def check_device_status():
    while True:
        now = datetime.now()
        for device_id in list(devices.keys()):
            last_seen = datetime.fromisoformat(devices[device_id]['last_seen'])
            # If device hasn't sent heartbeat in over 30 seconds, mark as offline
            if now - last_seen > timedelta(seconds=30):
                devices[device_id]['status'] = 'offline'
        save_devices()
        time.sleep(10)  # Check every 10 seconds

# Start background thread
threading.Thread(target=check_device_status, daemon=True).start()

@app.route('/')
def dashboard():
    return render_template('dashboard.html')

@app.route('/api/devices')
def get_devices():
    return jsonify(devices)

@app.route('/api/heartbeat', methods=['POST'])
def heartbeat():
    data = request.get_json()
    
    device_id = data.get('device_id')
    ip_address = data.get('ip_address')
    signal_strength = data.get('signal_strength', 'Unknown')
    
    if not device_id or not ip_address:
        return jsonify({'error': 'Missing device_id or ip_address'}), 400
    
    # Update device information
    devices[device_id] = {
        'device_id': device_id,
        'ip_address': ip_address,
        'last_seen': datetime.now().isoformat(),
        'status': 'online',
        'signal_strength': signal_strength
    }
    
    save_devices()
    return jsonify({'message': 'Heartbeat received'}), 200

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000, debug=True)
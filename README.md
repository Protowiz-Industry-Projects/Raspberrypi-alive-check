# 🖥️ Raspberry Pi Online Status Monitor Dashboard

## 📘 Overview

This project allows you to **monitor whether your Raspberry Pi devices are alive or not** using a **local web dashboard**.  
Each Raspberry Pi periodically sends a heartbeat signal (HTTP POST request) to a REST API endpoint running on a local server.  
The server updates the device's last seen time and status, which is then displayed on a **clean, live dashboard interface**.

Example dashboard view 👇  
✅ Online Devices, ❌ Offline Devices, ⏱️ Last Seen, 📶 Signal Strength — all in real time.

![Dashboard Preview](dashboard_preview.png)

## ⚙️ System Components

| Component | Description |
|------------|-------------|
| **Raspberry Pi (Client)** | Sends heartbeat data (device ID, IP, signal status) to the server. |
| **Flask Server (Backend)** | Receives heartbeats and maintains device status. |
| **Frontend Dashboard (Localhost Web App)** | Displays real-time data (online/offline devices). |

## 🔧 What It Does

1. Each Raspberry Pi runs a small Python script.
2. Every few seconds, the Pi sends a JSON heartbeat to your backend endpoint.
3. The backend updates the device list with:
   - Device ID  
   - IP Address  
   - Last Seen Timestamp  
   - Online/Offline Status  
   - Signal Strength
4. The dashboard auto-refreshes and shows the live status like this:

| Device ID | IP Address | Last Seen | Status | Signal Strength |
|------------|-------------|------------|----------|------------------|
| pi-001 | 192.168.29.247 | 11 sec ago | 🟢 Online | Good |

## 🧩 Requirements

- Python 3.x
- Flask
- Requests library
- Local network connection between server and Pi

## ▶️ Getting Started

### 1. Set Up the Server

1. Clone or download this repository
2. Install the required packages:
   ```bash
   pip install -r requirements.txt
   ```
3. Run the Flask server:
   ```bash
   python app.py
   ```
4. Access the dashboard at `http://localhost:5000`

### 2. Set Up Raspberry Pi Clients

On each Raspberry Pi you want to monitor:

1. Copy the [pi_client.py](pi_client.py) script to your Raspberry Pi
2. Install the required packages:
   ```bash
   pip install requests psutil
   ```
3. Run the client script:
   ```bash
   python pi_client.py --server http://YOUR_SERVER_IP:5000/api/heartbeat
   ```

Replace `YOUR_SERVER_IP` with the actual IP address of your server machine.

### 3. Customization Options

#### Server Options
- Change the port by modifying `app.run(port=5000)` in [app.py](app.py)
- Adjust the offline threshold by changing `timedelta(seconds=30)` in [app.py](app.py)

#### Client Options
- Specify a custom device ID: `python pi_client.py --device-id my-pi`
- Change heartbeat interval: `python pi_client.py --interval 30`
- Specify server URL: `python pi_client.py --server http://192.168.1.100:5000/api/heartbeat`

## 📁 Project Structure

```
raspberrypi-checker/
├── app.py              # Flask server application
├── pi_client.py        # Raspberry Pi client script
├── requirements.txt    # Python dependencies
├── devices.json        # Device data storage (created automatically)
├── templates/
│   └── dashboard.html  # Dashboard frontend
└── README.md           # This file
```

## 🛠️ API Endpoints

- `GET /` - Dashboard page
- `GET /api/devices` - Get all device statuses in JSON format
- `POST /api/heartbeat` - Receive heartbeat from a device

Heartbeat payload format:
```json
{
  "device_id": "pi-abc123",
  "ip_address": "192.168.1.100",
  "signal_strength": "Good"
}
```

## 📝 Notes

- Device data is stored in `devices.json` for persistence
- Devices are marked as offline if they haven't sent a heartbeat in 30 seconds
- The dashboard auto-refreshes every 5 seconds by default
- The client script generates a unique device ID based on the MAC address if not specified

## 🤝 Contributing

Feel free to fork this project and submit pull requests for improvements. Some ideas for enhancements:
- Add authentication
- Implement email/SMS alerts for offline devices
- Add historical data tracking
- Support for different device types
- Mobile-responsive design improvements

## 📄 License

This project is open source and available under the MIT License.


 http://192.168.29.111:5000


 python pi_client.py --server http://192.168.1.100:5000/api/heartbeat



@reboot python3 /home/pi/heartbeat.py &
#

https://www.waveshare.com/wiki/13.3inch_HDMI_LCD_(H)_(with_case)

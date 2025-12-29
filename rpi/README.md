Guardian Keychain — Raspberry Pi Companion

Overview

This folder contains example Python code to run on a Raspberry Pi with a camera module and buttons (e.g., On/Off and Help/SOS). The script runs a small Flask server that: 
- Serves an MJPEG camera stream
- Allows remote control (start/stop camera)
- Sends events when local buttons are pressed (POST to your server)

Requirements

- Raspberry Pi OS (Bullseye/Bookworm)
- Python 3.9+ recommended
- Camera connected and enabled (raspi-config or libcamera/picamera2 depending on setup)

Installation

1. Create a Python virtual environment

```bash
python -m venv .venv
source .venv/bin/activate
pip install -r requirements.txt
```

2. Copy `.env.example` to `.env` and update values

3. Run the service (for local testing)

```bash
python app.py
```

4. To run as a background service, configure the `guardian_rpi.service` systemd unit (see below)

Hardware wiring

- HELP button: Connect one side to a GPIO pin (default: 17) and the other to GND
- POWER toggle button: Connect to another GPIO pin (default: 27) and to GND
- Camera: Connect the camera ribbon to the camera port and enable camera in raspi-config

Default GPIO mapping (can be changed via `.env`):
- HELP_BUTTON_PIN=17
- POWER_BUTTON_PIN=27

Environment variables (`.env`)

- SERVER_URL: `https://your-server/api/rpi-events` (where the Pi will POST events)
- DEVICE_ID: unique id for the Pi
- API_KEY: optional shared secret header for authentication
- HELP_BUTTON_PIN, POWER_BUTTON_PIN: GPIO pins used for buttons

Systemd unit

Copy `guardian_rpi.service` to `/etc/systemd/system/guardian_rpi.service`, then:

```bash
sudo systemctl daemon-reload
sudo systemctl enable guardian_rpi
sudo systemctl start guardian_rpi
sudo journalctl -u guardian_rpi -f
```

Security

- Use HTTPS for SERVER_URL
- Use API_KEY to authenticate requests from the Pi

Notes

This example uses OpenCV for camera capture which works with USB cameras and some Pi cameras. If using the official camera module with libcamera, you may prefer `picamera2` (not included here). The code is purposely simple and should be extended to match your exact hardware and security needs.
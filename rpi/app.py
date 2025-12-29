#!/usr/bin/env python3
"""Simple Raspberry Pi companion service
- Serves MJPEG stream at /camera/stream
- Provides /camera/start and /camera/stop endpoints
- Monitors buttons and POSTs events to SERVER_URL

This is an example. Adjust pins, security, and camera code for your hardware.
"""

import os
import time
import threading
from flask import Flask, Response, jsonify, request
import requests
import cv2
from dotenv import load_dotenv

try:
    from gpiozero import Button
except Exception:
    Button = None

load_dotenv()

SERVER_URL = os.getenv('SERVER_URL')
DEVICE_ID = os.getenv('DEVICE_ID', 'raspi')
API_KEY = os.getenv('API_KEY', '')
HELP_PIN = int(os.getenv('HELP_BUTTON_PIN', '17'))
POWER_PIN = int(os.getenv('POWER_BUTTON_PIN', '27'))
CAM_INDEX = int(os.getenv('CAMERA_INDEX', '0'))
STREAM_PORT = int(os.getenv('STREAM_PORT', '8000'))

app = Flask(__name__)

camera_lock = threading.Lock()
camera = None
camera_running = False
frame = None

# Camera capture thread

def camera_loop():
    global camera, camera_running, frame
    cap = cv2.VideoCapture(CAM_INDEX)
    if not cap.isOpened():
        print('Camera could not be opened')
        camera_running = False
        return
    camera = cap
    camera_running = True
    print('Camera started')
    while camera_running:
        ret, img = cap.read()
        if not ret:
            print('Failed to read frame')
            time.sleep(0.1)
            continue
        # encode as JPEG
        ret, jpeg = cv2.imencode('.jpg', img, [int(cv2.IMWRITE_JPEG_QUALITY), 80])
        if ret:
            frame = jpeg.tobytes()
        time.sleep(0.03)  # ~30fps throttle
    cap.release()
    camera = None
    frame = None
    print('Camera stopped')


@app.route('/status', methods=['GET'])
def status():
    return jsonify({
        'device_id': DEVICE_ID,
        'camera_running': camera_running,
    })


@app.route('/camera/start', methods=['POST'])
def camera_start():
    global camera_running
    if camera_running:
        return jsonify({'status': 'already running'})
    t = threading.Thread(target=camera_loop, daemon=True)
    t.start()
    return jsonify({'status': 'started'})


@app.route('/camera/stop', methods=['POST'])
def camera_stop():
    global camera_running
    if not camera_running:
        return jsonify({'status': 'already stopped'})
    camera_running = False
    return jsonify({'status': 'stopping'})


def generate_mjpeg():
    global frame
    while True:
        if frame is None:
            time.sleep(0.05)
            continue
        chunk = (b'--frame\r\n'
                 b'Content-Type: image/jpeg\r\n\r\n' + frame + b'\r\n')
        yield chunk
        time.sleep(0.03)


@app.route('/camera/stream')
def camera_stream():
    if not camera_running:
        return jsonify({'error': 'camera not running'}), 503
    return Response(generate_mjpeg(), mimetype='multipart/x-mixed-replace; boundary=frame')


@app.route('/help', methods=['POST'])
def help_endpoint():
    data = {
        'device_id': DEVICE_ID,
        'event': 'help_pressed',
        'timestamp': int(time.time()),
    }
    headers = {'Authorization': f'Bearer {API_KEY}'} if API_KEY else {}
    try:
        if SERVER_URL:
            requests.post(SERVER_URL, json=data, headers=headers, timeout=5)
        else:
            print('No SERVER_URL configured, skipping POST', data)
    except Exception as e:
        print('Failed to post help event', e)
    return jsonify({'status': 'sent'})


def button_worker():
    if Button is None:
        print('gpiozero not available, skipping button monitoring')
        return

    def on_help():
        print('Help button pressed')
        # send local event
        try:
            requests.post(f'http://localhost:{STREAM_PORT}/help', timeout=2)
        except Exception:
            pass

        # send remote event
        data = {'device_id': DEVICE_ID, 'event': 'help_pressed', 'timestamp': int(time.time())}
        headers = {'Authorization': f'Bearer {API_KEY}'} if API_KEY else {}
        if SERVER_URL:
            try:
                requests.post(SERVER_URL, json=data, headers=headers, timeout=5)
            except Exception as e:
                print('Failed to post to SERVER_URL', e)

    help_btn = Button(HELP_PIN)
    help_btn.when_pressed = on_help

    def on_power():
        print('Power toggle pressed - toggling camera')
        global camera_running
        if camera_running:
            try:
                requests.post(f'http://localhost:{STREAM_PORT}/camera/stop', timeout=2)
            except Exception:
                camera_running = False
        else:
            try:
                requests.post(f'http://localhost:{STREAM_PORT}/camera/start', timeout=2)
            except Exception:
                pass

    power_btn = Button(POWER_PIN)
    power_btn.when_pressed = on_power


if __name__ == '__main__':
    # Start button worker in background
    t = threading.Thread(target=button_worker, daemon=True)
    t.start()

    # Optionally start camera automatically
    auto_start = os.getenv('AUTO_START_CAMERA', '1')
    if auto_start == '1':
        t2 = threading.Thread(target=camera_loop, daemon=True)
        t2.start()

    print(f'Starting Flask on 0.0.0.0:{STREAM_PORT}')
    app.run(host='0.0.0.0', port=STREAM_PORT)

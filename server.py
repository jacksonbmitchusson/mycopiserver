from datetime import datetime
from flask import Flask, abort, send_from_directory
from cv2 import VideoCapture, imwrite
from pytz import timezone
import threading, time
import os
import smbus2
import bme280

app = Flask(__name__)

addr = 0x77
bus = smbus2.SMBus(1)
calib_params = bme280.load_calibration_params(bus, address=addr)

cam = VideoCapture(0)

# seconds
delay = 60

output_path = '/home/onaquest/server-output'

recent_image_path = max(os.listdir(f'{output_path}/images/'))
print(f'recent_image_path: {recent_image_path}')

def read_pass(password_path): 
    with open(password_path) as f:
        return f.read()

def capture_data():
    while True:
        print('logginnggg')
        timestamp = datetime.now(timezone('America/Chicago')).strftime('%m-%d_%H-%M')
        capture_temphumid(timestamp)
        capture_image(timestamp)
        time.sleep(delay)

def capture_temphumid(timestamp):
    data = bme280.sample(bus, addr)
    t = (data.temperature * 9/5) + 32
    h = data.humidity
    p = data.pressure
    record_str = f'{timestamp} - {t:05.2f}°F {h:05.2f}% {p:05.2f} hPa'

    with open(f'{output_path}/environment_log.txt', 'a') as log:
        log.write('\n' + record_str)

def capture_image(timestamp):
    ret, frame = cam.read()
    if ret:
        path = f'{output_path}/images/{timestamp}.png'
        recent_image_path = path
        imwrite(path, frame)

@app.route('/<string:site_file>')
def get_file(site_file):
    print(f'requesting: {site_file}')
    filepath = f'site/{site_file}'
    if os.path.exists(filepath):
        with open(filepath) as f:
            return f.read()
    else:
        abort(404)

@app.route('/')
def get_root():
    return get_file('index.html')

# latest image captured
@app.route('/api/image/<string:input_password>')
def get_latest_image(input_password):
    if(input_password == password):
        recent_image_path = max(os.listdir(f'{output_path}/images/'))
        return send_from_directory(f'{output_path}/images', recent_image_path)

# latest temp/humid reading
@app.route('/api/env/')
def get_latest_env():
    last_n = []
    with open(f'{output_path}/environment_log.txt') as f:
        return f.read().split('\n')[-1]

password = read_pass('password.txt')
if __name__ == '__main__':
    print('starting...')
    threading.Thread(target=capture_data, daemon=True).start()
    app.run(host='0.0.0.0', port=80)

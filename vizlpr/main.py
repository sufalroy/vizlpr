import configparser
import datetime
import os

from camera.camera import Camera
from camera.sncvb630 import SNCVB630


def read_properties(file_path='../config/config.properties'):
    config = configparser.ConfigParser()
    config.read(file_path)
    return config['Camera']


if __name__ == "__main__":
    config = read_properties()

    camera_ip = config.get('camera_ip', '')
    output_dir = config.get('output_dir', os.path.join(os.getcwd(), 'output'))
    source_name = config.get('source_name', None)
    username = config.get('username', 'admin')
    password = config.get('password', 'admin')

    output_file_name = f"{source_name}_{datetime.datetime.now().strftime('%Y%m%d_%H%M%S')}.avi"
    output_path = os.path.abspath(os.path.join(output_dir, output_file_name))

    if not os.path.exists(output_dir):
        os.makedirs(output_dir)

    sony_camera = SNCVB630(camera_ip, username, password)

    sony_camera.set_resolution(640, 480)
    sony_camera.set_focus("focus", "auto", 0)
    sony_camera.set_infrared(False)
    sony_camera.set_frame_rate(30)
    sony_camera.set_exposure(7, 7)
    sony_camera.set_wide_dynamic_range("on")
    sony_camera.set_visibility_enhancer(2)
    sony_camera.set_backlight_compensation("off")

    source = f"rtsp://{username}:{password}@{camera_ip}:554/video1"
    with Camera(src=source, output_file=output_path) as camera:
        camera.start_capture()

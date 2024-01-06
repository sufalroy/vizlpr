import requests


class SNCVB630:

    def __init__(self, camera_ip, username, password):
        self.base_url = f"http://{camera_ip}"
        self.auth = (username, password)

    def send_request(self, endpoint, params=None):
        url = f"{self.base_url}/{endpoint}"
        response = requests.get(url, auth=self.auth, params=params)
        return response.text

    def set_infrared(self, mode):
        endpoint = "command/ircf.cgi"
        params = {"IrCutFilterMode": "manual", "IrCutFilterManual": "on" if mode else "off"}
        return self.send_request(endpoint, params)

    def set_focus(self, focus_mode, move_type, move_value):
        endpoint = "command/focuszoom.cgi"
        params = {"FzMove": f"{focus_mode},{move_type},{move_value}"}
        return self.send_request(endpoint, params)

    def set_resolution(self, width, height):
        endpoint = "command/camera.cgi"
        params = {"ImageSize1": f"{width},{height}"}
        return self.send_request(endpoint, params)

    def set_frame_rate(self, frame_rate):
        endpoint = "command/camera.cgi"
        params = {"FrameRate1": frame_rate}
        return self.send_request(endpoint, params)

    def set_exposure(self, min_exposure_time, max_exposure_time):
        endpoint = "command/imaging.cgi"
        params = {
            "ExposureMinExposureTime": min_exposure_time,
            "ExposureMaxExposureTime": max_exposure_time
        }
        return self.send_request(endpoint, params)

    def set_wide_dynamic_range(self, mode):
        endpoint = "command/imaging.cgi"
        params = {"WideDynamicRangeMode": mode}
        return self.send_request(endpoint, params)

    def set_visibility_enhancer(self, level):
        endpoint = "command/imaging.cgi"
        params = {"VisibilityEnhancer": level}
        return self.send_request(endpoint, params)

    def set_backlight_compensation(self, mode):
        endpoint = "command/imaging.cgi"
        params = {"BacklightCompensationMode": mode}
        return self.send_request(endpoint, params)

import requests


class LedController:

    rgb = None

    def __init__(self, ip, port, rgb="0,0,0"):
        self.ip = ip
        self.port = port
        self.set_rgb(rgb)

    def set_rgb(self, rgb):
        self.rgb = rgb
        rgb_ls = rgb.split(",")
        headers = {'Content-Type': 'application/x-www-form-urlencoded'}
        data = "r=" + rgb_ls[0] +"&g=" + rgb_ls[1] + "&b=" + rgb_ls[2]
        # requests.post('http://' + self.ip + ":" + str(self.port) + '/', data=data, headers=headers)

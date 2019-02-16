import requests


class LedController:

    rgb = None

    def __init__(self, ip, port, rgb="0,0,0"):
        self.ip = ip
        self.port = port
        self.set_rgb(rgb)

    def set_rgb(self, rgb, index=None):
        if self.ip is None:
            print("Led is not yet configured")
        else:
            self.rgb = rgb
            rgb_ls = rgb.split(",")

            headers = {'Content-Type': 'application/x-www-form-urlencoded'}
            data = "r=" + rgb_ls[0] +"&g=" + rgb_ls[1] + "&b=" + rgb_ls[2]
            if index is not None:
                print("index not none")
                data += "&index=" + str(index)
            requests.post('http://' + self.ip + ":" + str(self.port) + '/set', data=data, headers=headers)

"""c = LedController("192.168.0.121", 43432)
c.set_rgb("255,255,0", 0)
c.set_rgb("0,255,0", 1)
c.set_rgb("0,255,255", 2)"""
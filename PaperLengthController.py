#TODO: real number depending on rotary encoder
from LedController import LedController

amount_of_steps_per_cm = 10


class PaperLengthController:

    def __init__(self, on_paper_pushed_out, orchestrator):
        self.on_paper_pushed_out = on_paper_pushed_out
        if "led:0" in orchestrator.devices:
            led_ip = orchestrator.devices["led:0"]
        else:
            led_ip = None

        self.led = LedController(led_ip, 43432)
        self.reset()

    def device_update(self, devices):
        if "led:0" in devices:
            led_ip = devices["led:0"]
            self.led.ip = led_ip
            print("Updated LED IP")


    def set_paper_dimensions(self, width, length):
        self.paper_width = width
        #TODO: define max_paper_length differently
        self.min_paper_length = length
        self.max_paper_length = length + 20
        print("paper length should be in range " + str(self.min_paper_length) + " " + str(self.max_paper_length))
        self.active = True
        self.led.set_rgb("255,0,0")

    # TODO: needs to be called when the user cut off the paper (probably noticed by button press)
    def reset(self):
        self.active = False
        self.pushed_out = False
        self.paper_width = -1
        self.min_paper_length = -1
        self.max_paper_length = -1
        self.current_paper_length = -1
        if self.led is not None:
            self.led.set_rgb("255,0,0")

    def finish(self):
        if self.active:
            self.on_paper_pushed_out(self.current_paper_length)
            self.reset()

    def new_encoder_value(self, value):
        length = value / amount_of_steps_per_cm
        if self.active:
            self.current_paper_length = length
            if self.min_paper_length <= length <= self.max_paper_length:
                print("pushed out far enough")
                # self.on_paper_pushed_out()
                self.led.set_rgb("255,0,0")
            else:
                print("not in range")
                self.led.set_rgb("255,0,0")

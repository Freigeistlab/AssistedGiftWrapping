#TODO: real number depending on rotary encoder
from LedController import LedController

amount_of_steps_per_cm = 10

led_unit_name = "LedUnit0"

class PaperLengthController:

    in_range = False
    def __init__(self, orchestrator):
        self.orchestrator = orchestrator
        if led_unit_name in orchestrator.devices:
            led_ip = orchestrator.devices[led_unit_name]
        else:
            led_ip = None
        self.led = LedController(led_ip, 43432)
        self.reset()

    def device_update(self, devices):
        if led_unit_name in devices:
            led_ip = devices[led_unit_name]
            self.led.ip = led_ip
            self.led.set_rgb("255,0,0")
            print("Updated LED IP")

    def set_paper_dimensions(self, length):
        #TODO: define max_paper_length differently
        self.min_paper_length = length
        self.max_paper_length = length + 20
        print("paper length should be in range " + str(self.min_paper_length) + " " + str(self.max_paper_length))
        self.active = True
        self.led.set_rgb("255,0,0")

    # TODO: needs to be called when the user cut off the paper (probably noticed by button press)
    def reset(self):
        self.active = False
        self.in_range = False
        self.min_paper_length = -1
        self.max_paper_length = -1
        self.current_paper_length = -1
        if self.led is not None:
            self.led.set_rgb("255,0,0")

    """def finish(self):
        if self.active:
            self.on_paper_pushed_out(self.current_paper_length)
            self.reset()"""

    def new_encoder_value(self, value):
        length = value / amount_of_steps_per_cm
        if self.active:
            self.current_paper_length = length
            if not self.in_range:
                if self.min_paper_length <= length <= self.max_paper_length:
                    print("pushed out far enough")
                    # self.on_paper_pushed_out()
                    self.led.set_rgb("255,0,0")
                    self.orchestrator.finished_paper_prep()
            else:
                if not self.min_paper_length <= length <= self.max_paper_length:
                    print("not in range")
                    self.led.set_rgb("255,0,0")
                    self.orchestrator.paper_not_prepared()

            self.in_range = self.min_paper_length <= length <= self.max_paper_length

import math

encoder_radius = 2.5
encoder_steps = 2400
encoder_perimeter = 2*math.pi*2.5
amount_of_steps_per_cm = encoder_steps / encoder_perimeter
default_roll_out = 0  # in cms
revolution_bound = 50000
revolution_steps = 65536

class PaperLengthController:

    in_range = False

    def __init__(self, orchestrator):
        self.orchestrator = orchestrator
        self.led = orchestrator.led
        self.first_value = -1
        self.reset()

    def set_paper_dimensions(self, length):
        #TODO: define max_paper_length differently
        self.min_paper_length = length
        self.max_paper_length = length + 20
        print("paper length should be in range " + str(self.min_paper_length) + " " + str(self.max_paper_length))
        self.active = True
        self.led.set_rgb("0,0,0")

    # TODO: needs to be called when the user cut off the paper (probably noticed by button press)
    def reset(self):
        self.active = False
        self.in_range = False
        self.min_paper_length = -1
        self.max_paper_length = -1
        self.current_paper_length = -1
        if self.led is not None:
            self.led.set_rgb("255,0,0")

    def new_encoder_value(self, value):
        if self.active:
            if self.first_value == -1:
                self.first_value = value
                self.last_value = value

            if value - self.last_value > revolution_bound:
                self.first_value += revolution_steps
            elif self.last_value - value > revolution_bound:
                self.first_value -= revolution_steps

            length = (value - self.first_value) / amount_of_steps_per_cm
            length += default_roll_out

            self.current_paper_length = length
            print(self.min_paper_length)
            print(length)
            print(self.max_paper_length)
            if not self.in_range:
                if self.min_paper_length <= length <= self.max_paper_length:
                    print("pushed out far enough")
                    # self.on_paper_pushed_out()
                    self.orchestrator.finished_paper_prep()
                    self.led.set_rgb("0,255,0")
                else:
                    self.led.set_rgb("255,0,0")

            else:
                if not self.min_paper_length <= length <= self.max_paper_length:
                    print("not in range")
                    self.led.set_rgb("255,0,0")
                    self.orchestrator.paper_not_prepared()
            self.in_range = self.min_paper_length <= length <= self.max_paper_length
            self.last_value = value

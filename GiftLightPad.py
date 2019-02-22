from threading import Timer


class GiftLightPad:

    def __init__(self, orchestrator):
        self.led = orchestrator.led
        self.orchestrator = orchestrator
        self.active = False
        self.value = -1

    def set_value(self, value):
        if self.active:
            if value == 1:
                print("gift is present")
                t1 = Timer(1.0, self.timer,(value, 0))
                t1.start()
            else:
                self.orchestrator.gift_removed()
        self.value = value

    def timer(self, value, led_id):
        if value != self.value:
            self.led.set_rgb("0,0,0")
        else:
            if self.active:
                self.led.set_rgb("0,255,0",led_id)
                if led_id != 2:
                    t_next = Timer(1.0, self.timer,(value, led_id+1))
                    t_next.start()
                else:
                    print("Woop woop, gift placed!")
                    self.active = False
                    self.orchestrator.gift_placed()
        return
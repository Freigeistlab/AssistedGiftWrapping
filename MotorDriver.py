from threading import Thread
import time


class MotorDriver(Thread):

    def __init__(self, on_pushed_paper_out):
        Thread.__init__(self)
        self.on_pushed_paper_out = on_pushed_paper_out
        self.paper_length = -1
        self.rotations = -1

    def set_paper_length(self, paper_length):
        self.paper_length = paper_length

    def run(self):
        print("______________________________________________________")
        print("Pushing out the paper...")
        time.sleep(3)
        print("______________________________________________________")
        self.on_pushed_paper_out()
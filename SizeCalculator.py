from threading import Thread
from random import randint
import time


class SizeCalculator(Thread):

    def __init__(self, on_size_calculated):
        Thread.__init__(self)
        self.on_size_calculated = on_size_calculated
        self.gift_width = -1
        self.gift_height = -1
        self.gift_depth = -1
        self.paper_width = -1
        self.paper_height = -1

    def run(self):
        print("______________________________________________________")
        print("Calculating size...")
        time.sleep(2)
        print("______________________________________________________")
        self.gift_width = randint(10, 40)
        self.gift_height = randint(8, 22)
        self.gift_depth = randint(5, 18)
        self.paper_width = randint(self.gift_width+10, self.gift_width+40)
        self.paper_height = randint(self.gift_height+10, self.gift_height+40)
        self.on_size_calculated()
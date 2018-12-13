from threading import Thread
from random import randint
import time

class SizeCalculator(Thread):

    on_size_calculated = None

    def __init__(self, on_size_calculated):
        Thread.__init__(self)
        self.on_size_calculated = on_size_calculated

    def run(self):
        print("______________________________________________________")
        print("Calculating size...")
        time.sleep(2)
        print("______________________________________________________")
        self.width = randint(10, 40)
        self.height = randint(8, 22)
        self.depth = randint(5, 18)
        self.on_size_calculated()
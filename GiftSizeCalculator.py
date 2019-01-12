from threading import Thread
from random import randint
import time
import operator

class GiftSizeCalculator(Thread):

    def __init__(self, on_size_calculated):
        Thread.__init__(self)
        self.on_size_calculated = on_size_calculated
        self.gift_width = -1
        self.gift_height = -1
        self.gift_depth = -1
        self.paper_width = -1
        self.paper_height = -1

    def set_width(self, width):
        self.gift_width = width

    def set_height(self, height):
        self.gift_height = height

    def set_depth(self, depth):
        self.gift_depth = depth

    def run(self):
        print("______________________________________________________")
        print("Calculating size...")
        time.sleep(2)
        print("______________________________________________________")
        """width = randint(15, 40)
        height = randint(8, 22)
        depth = randint(5, 18)"""
        dimensions = {
            "width": randint(15, 40),
            "height": randint(8,22),
            "depth": randint(5,18),
        }
        dimensions = sorted(dimensions.items(), key=operator.itemgetter(1))
        print(dimensions)
        self.gift_width = dimensions[2][1]
        self.gift_height = dimensions[1][1]
        self.gift_depth = dimensions[0][1]
        print("width " + str(self.gift_width))
        print("height " + str(self.gift_height))
        print("depth " + str(self.gift_depth))
        self.paper_width = self.gift_width + self.gift_depth * 2 + 10
        self.paper_height = self.gift_height * 2 + self.gift_depth * 2 + 10
        self.on_size_calculated()
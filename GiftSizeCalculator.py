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
        self.paper_width = 50
        self.paper_height = -1
        self.paper_overlap = 3 # how many cms the wrapping paper needs to overlap for the gift

    def set_width(self, width):
        print("set width to " + str(width))
        self.gift_width = width

    def set_height(self, height):
        print("set height to " + str(height))
        self.gift_height = height

    def set_depth(self, depth):
        print("set depth to " + str(depth))
        self.gift_depth = depth

    def generate_mock_values(self):
        """dimensions = {
            "width": randint(30, 40),
            "height": randint(15,22),
            "depth": randint(10,18),
        }"""
        self.set_width(30)
        self.set_height(15)
        self.set_depth(6)

    def run(self):

        self.generate_mock_values()
        while (self.gift_width == -1 or self.gift_height == -1 or self.gift_depth == -1):
            pass

        print("______________________________________________________")
        print("Calculating size...")
        time.sleep(1)
        print("______________________________________________________")
        dimensions = {
            "width": self.gift_width,
            "height": self.gift_height,
            "depth": self.gift_depth,
        }
        dimensions = sorted(dimensions.items(), key=operator.itemgetter(1))
        print(dimensions)
        self.gift_width = dimensions[2][1]
        self.gift_height = dimensions[1][1]
        self.gift_depth = dimensions[0][1]
        print("width " + str(self.gift_width))
        print("height " + str(self.gift_height))
        print("depth " + str(self.gift_depth))
        if self.gift_width + (2 * self.gift_depth) <= self.paper_width:
            self.paper_height = self.gift_height * 2 + self.gift_depth * 2 + 2 * self.paper_overlap
        else:
            # gift is too wide
            # check if it is also too high --> if so, we cannot pack this gift
            if self.gift_height + (2 * self.gift_depth) > self.paper_width:
                print("Gift is too big")
                exit()
            else:
                # swap gift width and height
                tmp = self.gift_width
                self.gift_width = self.gift_height
                self.gift_height = tmp
                self.paper_height = self.gift_height * 2 + self.gift_depth * 2 + 2 * self.paper_overlap

        self.on_size_calculated()
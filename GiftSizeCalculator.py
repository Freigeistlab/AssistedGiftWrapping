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
        self.gift_width = width

    def set_height(self, height):
        self.gift_height = height

    def set_depth(self, depth):
        self.gift_depth = depth

    def generate_mock_values(self):
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
        #self.paper_width = self.gift_width + self.gift_depth * 2 + 10
        if self.gift_width + (2 * self.gift_depth) <= self.paper_width:
            self.paper_height = self.gift_height * 2 + self.gift_depth * 2 + 2 * self.paper_overlap
        else:
            # gift is too wide
            # check if it is also too high --> if so, we cannot pack this gift
            if self.gift_height + (2 * self.gift_depth) <= self.paper_width:
                print("Gift is too big")
                exit()
            else:
                # swap gift width and height
                tmp = self.gift_width
                self.gift_width = self.gift_height
                self.gift_height = tmp
                self.paper_height = self.gift_height * 2 + self.gift_depth * 2 + 2 * self.paper_overlap

    def run(self):
        print("______________________________________________________")
        print("Calculating size...")
        time.sleep(2)
        print("______________________________________________________")
        """width = randint(15, 40)
        height = randint(8, 22)
        depth = randint(5, 18)"""
        self.generate_mock_values()
        self.on_size_calculated()
from threading import Thread, Timer
import time
import operator

width_sensor_dist = 35
height_sensor_dist = 58
depth_sensor_dist = 51
gift_present_sensor_dist = 85
noise = 2


class GiftSizeCalculator:

    def __init__(self, on_size_calculated, gift_placed, led):
        self.on_size_calculated = on_size_calculated
        self.gift_placed = gift_placed
        self.gift_width = -1
        self.gift_height = -1
        self.gift_depth = -1
        self.gift_distance = -1
        self.paper_width = 50
        self.paper_height = -1
        self.paper_overlap = 3 # how many cms the wrapping paper needs to overlap for the gift
        self.finished = False
        self.measuring = False
        self.active = False
        self.dist_active = False
        self.led = led

    def generate_mock_values(self):
        print("Generating mocks")
        self.gift_width = 30
        self.gift_height = 20
        self.gift_depth = 10
        self.paper_height = 64
        """self.active = True
        self.set_width(9)
        self.set_height(39)
        self.set_depth(53)"""

    def set_width(self, w):
        if self.active:
            if width_sensor_dist - noise <= w <= width_sensor_dist + noise:
                # this is the default distance
                self.gift_width = -1
            else:
                width = width_sensor_dist - w
                print("set width to " + str(width))
                self.gift_width = width
                self.check_dimensions()

    def set_height(self, h):
        if self.active:
            if height_sensor_dist - noise <= h <= height_sensor_dist + noise:
                self.gift_height = -1
                # initial value
            else:
                height = height_sensor_dist - h
                print("set height to " + str(height))
                self.gift_height = height
                self.check_dimensions()

    def set_depth(self, d):
        if self.active:
            if depth_sensor_dist - noise <= d <= depth_sensor_dist + noise:
                self.gift_depth = -1
                # initial value
            else:
                depth = depth_sensor_dist - d
                print("set depth to " + str(depth))
                self.gift_depth = depth
                self.check_dimensions()

    def set_distance_to_gift(self, dist):
        if self.dist_active:
            if gift_present_sensor_dist - noise <= dist <= gift_present_sensor_dist + noise:
                self.gift_distance = -1
                # initial value
            else:
                dist = gift_present_sensor_dist - dist
                print("gift distance: " + str(dist))
                self.gift_distance = dist
                t1 = Timer(1.0, self.timer_dist, (dist,0))
                t1.start()

    def timer(self, w, h, d, led_id):
        if w != self.gift_width or h != self.gift_height or d != self. gift_depth:
            self.led.set_rgb("0,0,0")
            # set LEDs to black
        else:
            if self.active:
                self.led.set_rgb("0,255,0",led_id)
                if led_id != 2:
                    t_next = Timer(1.0, self.timer, (w, h, d,led_id+1))
                    t_next.start()
                else:
                    print("Woop woop, size measured!")
                    self.active = False
                    self.calc_dimensions(w,h,d)
        return

    def timer_dist(self, dist, led_id):
        if dist != self.gift_distance:
            self.led.set_rgb("0,0,0")
        else:
            if self.dist_active:
                self.led.set_rgb("0,255,0",led_id)
                if led_id != 2:
                    t_next = Timer(1.0, self.timer_dist, (dist,led_id+1))
                    t_next.start()
                else:
                    print("Woop woop, gift placed!")
                    self.dist_active = False
                    self.gift_placed()
        return

    def check_dimensions(self):
        if not (self.gift_width == -1 or self.gift_height == -1 or self.gift_depth == -1):
            print("Started new timer")
            t1 = Timer(1.0, self.timer, (self.gift_width, self.gift_height, self.gift_depth,0))
            t1.start()

    def calc_dimensions(self, w,h,d):
        print("______________________________________________________")
        print("Calculating size...")
        time.sleep(1)
        print("______________________________________________________")
        dimensions = {
            "width": w,
            "height": h,
            "depth": d,
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
        return
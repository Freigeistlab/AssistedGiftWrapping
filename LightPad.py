from threading import Thread
from random import randint
import time

class LightPad(Thread):
    id = None
    on_lightval_changed = None
    def __init__(self, on_lightval_changed, id):
        Thread.__init__(self)
        self.id = id
        self.on_lightval_changed = on_lightval_changed

    def run(self):
        lastVal = 0
        while(True):
            time.sleep(1)
            val = randint(0, 30)
            #val = 2
            if val != lastVal:
                #print('Lightpad Value changed %d for id %d' % (val, self.id))
                self.on_lightval_changed(self.id, val)
                lastVal = val
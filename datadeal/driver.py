import time
import numpy as np
from setting import *
np.random.seed(seed)
from datadeal.order import Order

class Driver:
    def __init__(self, location):
        self.severedOrder = []
        self.x, self.y = location
        self.relaxTime = 0


    def isAccept(self, order: Order):
        if (abs(self.x - order.pickX) + abs(self.y - order.pickY)) / order.speed > takeTime:
            return False
        return True

    def serve(self, order: Order, currentTime):
        order.available = False
        self.severedOrder.append(order)
        pickTime = 0 if order.speed == 0 else (abs(self.x - order.pickX) + abs(self.y - order.pickY)) / order.speed
        self.relaxTime = currentTime + order.dropoffTime - order.pickTime + pickTime
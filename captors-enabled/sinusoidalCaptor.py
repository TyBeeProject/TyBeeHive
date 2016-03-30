from random import random
from time import time
from math import sin, pi

class Captor():
    id = 3
    def Captor():
        self.id = 3
        

    def callback(self):
        return 48*(1+sin(2*pi*time()/1000.0)) + 2*random()

    def getId(self):
        return self.id

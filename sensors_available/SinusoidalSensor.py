
from time import time
from math import sin, pi
from random import random

from main import AbstractSensor


class RandomSensor(AbstractSensor):
    def __init__(self, sensor_id, name=''):
        super(RandomSensor, self).__init__(sensor_id, name)

    def callback(self):
        return 48*(1+sin(2*pi*time()/1000.0)) + 2*random()

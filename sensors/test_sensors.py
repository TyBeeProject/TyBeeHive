from random import random
from math import sin, pi
from time import time

from sensors import AbstractSensor


class RandomSensor(AbstractSensor):
    def __init__(self, sensor_id, name=''):
        super(RandomSensor, self).__init__(sensor_id, name)

    def callback(self):
        return 48*(1+sin(2*pi*time()/1000.0)) + 2*random()


class RandomWalkSensor(AbstractSensor):
  def __init__(self, sensor_id, name=''):
    super(RandomWalkSensor, self).__init__(sensor_id, name)

  def callback(self):
    try:
      f = open('randomWalk', 'r')
      prev = int(f.read())
      f.close()
    except:
      prev = 50

    new = prev + random() * 100 - 50
    if new < 0:
      new = 0
    elif new > 100:
      new = 100

    try:
      f = open('randomWalk', 'w')
      f.write(new)
      f.close()
    except:
      pass

    return new
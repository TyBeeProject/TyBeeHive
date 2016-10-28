from abc import ABC, abstractmethod
from general_sensors import *
from test_sensors import *

class AbstractSensor(ABC):
    """
    A template for the Sensor class
    """
    def __init__(self, sensor_id, name=""):
        self.id = sensor_id
        self.name = name

    @abstractmethod
    def callback(self):
        return 0

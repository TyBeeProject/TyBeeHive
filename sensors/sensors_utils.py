from abc import ABC, abstractmethod


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

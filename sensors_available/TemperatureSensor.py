
from main import AbstractSensor
import Adafruit_Python_DHT

sensor_type = Adafruit_Pyhon_DHT.DHT22

class TemperatureSensor(AbstractSensor):
    def __init__(self, sensor_id, pin, name=''):
        super(TemperatureSensor, self).__init__(sensor_id, name)
        self.sensor_type = sensor_type
        self.pin = pin

    def callback(self):
        moisture, temperature = Adafruit_Python_DHT.read(self.sensor_type, self.pin)
        if temperature is None:
            return 0
        return temperature
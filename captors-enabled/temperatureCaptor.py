import Adafruit_Python_DHT

pin = 14
sensor = Adafruit_Pyhon_DHT.DHT22


class Captor():
  id = 4
  def Captor():
    self.id = 4
    
    
  def callback(self):
    moisture,temperature = Adafruit_Python_DHT.read(sensor,pin)
    if temperature is None:
      return 0
    return temperature
    
  def getiId(self):
    return self.id

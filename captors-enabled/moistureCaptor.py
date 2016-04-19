import Adafruit_Python_DHT

pin = 14
sensor = Adafruit_Pyhon_DHT.DHT22

class Captor():
  id = 5
  def Captor():
    self.id = 5
    
    
  def callback(self):
    moisture,temperature = Adafruit_Python_DHT.read(sensor,pin)
    if moisture is None:
      return 0
    return moisture
    
  def getiId(self):
    return self.id

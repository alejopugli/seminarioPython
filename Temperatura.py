import Adafruit_DHT
import date

class Temperatura:
   def __init__(self, pin=17, sensor=Adafruit_DHT.DHT11):
      self._sensor = sensor
      self._data_pin = pin

   def datosSensor(self):
      humedad, temperatura = Adafruit_DHT.read_retry(self._sensor, self._data_pin)
      return {'temperatura': temperatura, 'humedad': humedad, 'fecha': date.today()}
import Adafruit_DHT
import datetime

class Temperatura:
   def __init__(self, pin=17, sensor=Adafruit_DHT.DHT11):
      self._sensor = sensor
      self._data_pin = pin

   def formatearFecha():
      day = (datetime.datetime.today().ctime()).split(' ')
      return("{} {} {}, {}".format(day[0],day[2],day[1],int(day[4])%100))

   def datosSensor(self):
      humedad, temperatura = Adafruit_DHT.read_retry(self._sensor, self._data_pin)
      return {'temperatura': temperatura, 'humedad': humedad, 'fecha': self.formatearFecha()}
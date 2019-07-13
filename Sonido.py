import RPi.GPIO as GPIO

class Sonido:
   def __init__(self, canal=22):
      self._canal = canal
      GPIO.setmode(GPIO.BCM)
      GPIO.setup(self._canal, GPIO.IN)
      GPIO.setwarnings(False)
      GPIO.add_event_detect(self._canal, GPIO.RISING)

   def detectaSonido(self):
      return GPIO.event_detected(self._canal)
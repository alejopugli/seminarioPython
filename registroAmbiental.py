import sys
import time
import Adafruit_DHT as adht
import json
import date

"""
MIEMBROS DEL GRUPO:
CRIS, SEBASTIAN AGUSTIN
PUGLIESE, ALEJO EZEQUIEL
PISONI, FELIPE
"""

OFICINAS = 10

def leerADHT():
   humedad, temperatura, fecha = adht.read_retry(),date.today()
   return {'temperatura':temperatura,'humedad':humedad,'fecha':fecha}

def leerArch():
   try:
      arch = open('data.json','r+')
   except PermissionError:
      print('El archivo no puede ser abierto con sus permisos!')
   except FileNotFoundError:
      print('El archivo no se encontró.')     
   else:
      return arch
   return None

def leerOficinas():
   for o in range(1,OFICINAS):
      dic['oficina'+str(o)] = leerADHT()
   return dic

def main(argv):
   arch = leerArch()
   if (arch is not None):
      json.dump(leerOficinas(),arch,indent=4)
      while True:
         time.sleep(60)
         json.dump(leerOficinas(),arch,indent=4)
      close(arch)
   else:
      print('Error en el archivo')

if __name__ == "__main__":
    main(sys.argv[1:])
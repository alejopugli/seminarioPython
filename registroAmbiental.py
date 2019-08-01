import sys
import time
import json
import datetime
import Temperatura

"""
MIEMBROS DEL GRUPO:
CRIS, SEBASTIAN AGUSTIN
PUGLIESE, ALEJO EZEQUIEL
PISONI, FELIPE
"""

def leerArch():
   try:
      arch = open('data.json','r+')
   except PermissionError:
      print('¡El archivo no puede ser abierto con sus permisos!')
   except FileNotFoundError:
      print('El archivo no se encontró.')     
   else:
      return arch
   return None

def leerOficinas(ofi,temp,dic):
   for o in range(1,ofi):
      dic["oficina"+str(o)].apend(temp.datosSensor())
   return dic

def main(argv):
   ofi = argv[0]
   t = Temperatura()
   arch = leerArch()
   if (arch is not None):
      datos = json.load(arch)
      while True:
         leerOficinas(ofi,t,datos)
         print('Esperando 1')
         time.sleep(60)
      close(arch)
   else:
      print('Error en el archivo, saliendo...')

if __name__ == "__main__":
    main(sys.argv[1:])
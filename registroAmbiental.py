import sys
import time
import json
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
      print('El archivo no puede ser abierto con sus permisos!')
   except FileNotFoundError:
      print('El archivo no se encontró.')     
   else:
      return arch
   return None

def leerOficinas():
   for o in range(1,OFICINAS):
      dic["oficina"+str(o)] = leerADHT()
   return dic

def main(argv):
   t = Temperatura()
   arch = leerArch()
   if (arch is not None):
      json.dump(t.datosSensor(),arch,indent=4)
      while True:
         time.sleep(60)
         json.dump(t.datosSensor(),arch,indent=4)
      close(arch)
   else:
      print('Error en el archivo')

if __name__ == "__main__":
    main(sys.argv[1:])
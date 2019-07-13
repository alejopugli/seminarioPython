import Matriz
import Sonido
import Temperatura

def main(args):
   matriz = Matriz(numero_matrices=2, ancho=16)
   sonido = Sonido()
   amb = Temperatura()
   while True:
      if (sonido.detectaSonido())
         matriz.mostrarMensaje(amb.leerADHT())

if __name__ == "__main__":
   main(argv[:1])
import sys
import PySimpleGUI as sg
import random
import string

"""
MIEMBROS DEL GRUPO:
CRIS, SEBASTIAN AGUSTIN
PUGLIESE, ALEJO EZEQUIEL
PISONI, FELIPE
"""


BOX_SIZE = 25 #constante que representa el tamaño de un "casillero"
COLORES = ['ROJO','VERDE','AZUL','AMARILLO','ROSA','VIOLETA']

#ventana de la sopa de letras:
sopa_layout = [
                [sg.Graph((800,800), (0,450), (450,0), key='_GRAPH_', change_submits=True, drag_submits=False)]
              ]

sopa_window = sg.Window('SOPA DE LETRAS', ).Layout(sopa_layout).Finalize()


config_layout = [
                   [sg.Text('PALABRAS'),sg.Input(size=(21,1)),sg.Button('Agregar')],
                   [sg.Listbox(values=[],size=(40,4))],
                   [sg.Text('COLORES SUSTANTIVOS'),sg.InputCombo(values=COLORES,default_value=COLORES[0],size=(15,1))],     
                   [sg.Text('COLORES ADJETIVOS'),sg.InputCombo(values=COLORES,default_value=COLORES[1],size=(15,1))],      
                   [sg.Text('COLORES VERBOS'),sg.InputCombo(values=COLORES,default_value=COLORES[2],size=(15,1))],                                              
                   [sg.Text('ORIENTACION'),sg.InputCombo(values=['HORIZONTAL','VERTICAL'],size=(15,1))],   
                   [sg.Text('OFICINA'),sg.InputCombo(values=[None],size=(15,1))],                 
                   [sg.Checkbox('SOLO MINUSCULAS')],                 
                   [sg.Checkbox('AYUDA')],
                ]
config_window = sg.Window('CONFIGURACION', ).Layout(config_layout)
config_window.Read()
    

def generar_sopa(minusculas=False,filas=16,columnas=16):
    g = sopa_window.FindElement('_GRAPH_')
    if minusculas:
        mayus_minus=string.ascii_lowercase
    else:
        mayus_minus=string.ascii_uppercase
    for row in range(filas):
        for col in range(columnas):
                g.DrawRectangle((col * BOX_SIZE + 5, row * BOX_SIZE + 3), (col * BOX_SIZE + BOX_SIZE + 5, row * BOX_SIZE + BOX_SIZE + 3), line_color='black') #se dibuja cuadrado
                box_x = (col * BOX_SIZE + 5) // BOX_SIZE
                box_y = (row * BOX_SIZE + 3) // BOX_SIZE
                letter_location = (box_x * BOX_SIZE + 18, box_y * BOX_SIZE + 17)
                g.DrawText('{}'.format(random.choice(mayus_minus)), letter_location, font='Courier 25') #se dibuja letra adentro del cuadrado


def main(argv):

    generar_sopa()
    
    while True:
        event, values = sopa_window.Read()
        print(event, values)
        if event is None or event == 'Exit':
            break
        mouse = values['_GRAPH_']

        if event == '_GRAPH_':
            if mouse == (None, None):
                continue
            box_x = mouse[0]//BOX_SIZE
            box_y = mouse[1]//BOX_SIZE
            letter_location = (box_x * BOX_SIZE + 18, box_y * BOX_SIZE + 17)
            print(box_x, box_y)

    sopa_window.Close()


if __name__ == "__main__":
    main(sys.argv[1:])


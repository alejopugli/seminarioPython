#!/usr/bin/env python36

import buscador_palabras as bp
import sopa_de_letras as sl
import PySimpleGUI as sg

"""
MIEMBROS DEL GRUPO:
CRIS, SEBASTIAN AGUSTIN
PUGLIESE, ALEJO EZEQUIEL
PISONI, FELIPE
"""
def masLarga(dic):
    sortedwords = sorted(dic.keys(), key=len, reverse=True)
    return len(sortedwords[0])

#ventana configuracion:
config_layout = [
                   [sg.Text('PALABRAS'),sg.Input(size=(35,1),key='PALABRA'),sg.Button('Agregar',bind_return_key=True)],
                   [sg.Listbox(values=[],size=(55,6),key='LISTA',select_mode="LISTBOX_SELECT_MODE_single", bind_return_key=True)],
                   [sg.Button('Eliminar')],
                   [sg.Text('\n')],
                   [sg.Text(' '*5+'COLOR'),sg.InputCombo(values=COLORES,default_value=COLORES[0],size=(10,1),key='COL_SUS'),sg.InputCombo(values=COLORES,default_value=COLORES[1],size=(10,1),key='COL_ADJ'),sg.InputCombo(values=COLORES,default_value=COLORES[2],size=(10,1),key='COL_VER')],                 
                   [sg.Text('\n')],
                   [sg.Text(' '*27+'AYUDA'),sg.InputCombo(values=['TOTAL','PARCIAL','DESACTIVADA'],default_value='DESACTIVADA',size=(15,1),key='AYUDA')],
                   [sg.Text(' '*17+'ORIENTACION'),sg.InputCombo(values=['HORIZONTAL','VERTICAL'],size=(15,1),key='ORIENTACION')],
                   [sg.Text(' '*26+'FUENTE'),sg.InputCombo(values=FUENTES,size=(15,1),key='FUENTE')],
                   [sg.Text(' '*26+'OFICINA'),sg.InputCombo(values=[None],size=(15,1))], #values=list(oficinas.keys())                
                   [sg.Text('\n')],
                   [sg.Checkbox('SOLO MINUSCULAS',key='MINUSCULAS')],
                   [sg.Button('LISTO',pad=(179,1))]
                ]
config_window = sg.Window('CONFIGURACION', background_color=None).Layout(config_layout)

palabras= []                                                #lista de palabras para la sopa de letras
contador = {'sustantivo':0,'adjetivo':0,'verbo':0 }         #contador de cada tipo
dic = {}                                                    #diccionario que va a almacenar las palabras por tipos 

while True:
    event , values = config_window.Read()
    
    if event == 'Agregar':
        palabra = values['PALABRA'].lower()
        if articulo != None :
            if palabra not in config_window.FindElement('LISTA').GetListValues():
                if (bp.buscar(palabra,dic,contador)):
                    palabras.append(palabra)
                    config_window.FindElement('LISTA').Update(values=palabras)
                    dic[palabra]={'tipo':tipo,'descripcion':descripcion}
                    contador[tipo] += 1

    elif event == 'LISTA': #si se hace doble clcik en un elemento de la lista se muestra la definicion de la palabra
        sg.Popup('Definicion',dic[values['LISTA'][0]]['descripcion'])
    
    elif event == 'Eliminar':
        if len(list(dic.keys())) > 0:
            contador[ dic[values['LISTA'][0]] ['tipo'] ] -= 1
            del dic[values['LISTA'][0]]
            config_window.FindElement('LISTA').Update(values=list(dic.keys()))
    
    elif event == 'LISTO':
            #contadores de tipos:
            c_sustantivos = int(values['SUSTANTIVOS']) #cantidad sustantivos,adjetivos,verbos
            c_adjetivos = int(values['ADJETIVOS'])
            c_verbos = int(values['VERBOS'])
            #si tengo al menos una palabra
            if (c_sustantivos + c_adjetivos + c_verbos < 0):
                ayuda = values['AYUDA']
                minusculas = values['MINUSCULAS']
                fuente = values['FUENTE']
                orientacion = values['ORIENTACION']
                config_window.Close()
                sl.generar_sopa(dic,masLarga(dic),orientacion,fuente,minusculas)
                break
            else:
                sg.Popup("Ingrese al menos una palabra valida")
    elif event is None:
        break

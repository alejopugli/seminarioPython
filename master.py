#!/usr/bin/env python36

import buscador_palabras as bp
import sopa_de_letras as sl
import PySimpleGUI as sg
import string
import json

"""
MIEMBROS DEL GRUPO:
CRIS, SEBASTIAN AGUSTIN
PUGLIESE, ALEJO EZEQUIEL
PISONI, FELIPE
"""

COLORES = ['ROJO','VERDE','AZUL','AMARILLO','ROSA','VIOLETA']
FUENTES = [ 'Arial' ,'Courier', 'Comic', 'Fixedsys','Times','Verdana','Helvetica' ]

def masLarga(dic):
    sortedwords = sorted(dic.keys(), key=len, reverse=True)
    return len(sortedwords[0])

#ventana configuracion:
config_layout = [
                    [sg.Text('PALABRAS'),sg.Input(size=(35,1),key='PALABRA'),sg.Button('Agregar',bind_return_key=True)],
                    [sg.Listbox(values=[],size=(55,6),key='LISTA',select_mode="LISTBOX_SELECT_MODE_single", bind_return_key=True)],
                    [sg.Button('Eliminar')],
                    [sg.Text(' '*19+'SUSTANTIVOS'+' '*2),sg.Text('ADJETIVOS'+' '*6),sg.Text('VERBOS')],
                    [sg.Text(' '*5+'COLOR'),sg.InputCombo(values=COLORES,default_value=COLORES[0],size=(10,1),key='COL_SUS'),sg.InputCombo(values=COLORES,default_value=COLORES[1],size=(10,1),key='COL_ADJ'),sg.InputCombo(values=COLORES,default_value=COLORES[2],size=(10,1),key='COL_VER')],                 
                    [sg.Text(' '*18+'MINUSCULAS'),sg.InputCombo(values=['MINUSCULAS','MAYUSCULAS'],size=(15,1),key='MINUSCULAS')],
                    [sg.Text(' '*17+'ORIENTACION'),sg.InputCombo(values=['HORIZONTAL','VERTICAL'],size=(15,1),key='ORIENTACION')],
                    [sg.Text(' '*26+'FUENTE'),sg.InputCombo(values=FUENTES,size=(15,1),key='FUENTE')],
                    [sg.Text(' '*26+'OFICINA'),sg.InputCombo(values=[None],size=(15,1))], #values=list(oficinas.keys())                
                    [sg.Text('\n')],
                    [sg.Button('LISTO',pad=(179,1))]
                ]
config_window = sg.Window('CONFIGURACION', background_color=None).Layout(config_layout)

contador = {'sustantivo':0,'adjetivo':0,'verbo':0 }         #contador de cada tipo
dic = {}                                                    #diccionario que va a almacenar las palabras por tipos 

while True:
    event , values = config_window.Read()
    
    if event == 'Agregar':
        ok = False
        palabra = values['PALABRA'].lower()
        if palabra != '' :
            if palabra not in config_window.FindElement('LISTA').GetListValues():
                if (bp.buscar(palabra,dic,contador)):
                    config_window.FindElement('LISTA').Update(values=list(dic.keys()))
                    contador[dic[palabra]['tipo']] += 1
            else:
                sg.Popup('La palabra ya fue ingresada, intente con otra')
    elif event == 'LISTA':                                                  #si se hace doble clcik en un elemento de la lista se muestra la definicion de la palabra
        sg.Popup('Definicion',dic[values['LISTA'][0]]['descripcion'])
    
    elif event == 'Eliminar':
        if len(list(dic.keys())) > 0:
            contador[ dic[values['LISTA'][0]] ['tipo'] ] -= 1
            del dic[values['LISTA'][0]]
            config_window.FindElement('LISTA').Update(values=list(dic.keys()))
    
    elif event == 'LISTO':
            
            #si tengo al menos una palabra
            if (dic):
                minusculas = values['MINUSCULAS']
                fuente = values['FUENTE']
                orientacion = values['ORIENTACION']
                colores = [values['COL_SUS'],values['COL_ADJ'],values['COL_VER']]
                cantidades = [contador['sustantivo'],contador['adjetivo'], contador['verbo']]
                config_window.Close()
                sl.jugar(dic,masLarga(dic),colores,cantidades,orientacion,fuente,minusculas)
                break
            else:
                sg.Popup("Ingrese al menos una palabra valida")
    elif event is None:
        break

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
    '''esta funcion devuelve la palabra mas larga entre las ingresadas'''
    sortedwords = sorted(dic.keys(), key=len, reverse=True)
    return len(sortedwords[0])

def cargarJSON():
    arch = open('datos-oficinas.json','r')
    if arch is not None:
        datosJson = json.load(arch)
        return datosJson
    else:
        return None

oficinas = cargarJSON()
#ventana configuracion:
config_layout = [
                    [sg.Text('PALABRAS'),sg.Input(size=(35,1),key='PALABRA'),sg.Button('Agregar',bind_return_key=True)],
                    [sg.Listbox(values=[],size=(55,6),key='LISTA',select_mode="LISTBOX_SELECT_MODE_single", bind_return_key=True)],
                    [sg.Button('Eliminar')],
                    [sg.Text(' '*19+'SUSTANTIVOS'+' '*2),sg.Text('ADJETIVOS'+' '*6),sg.Text('VERBOS')],
                    [sg.Text(' '*5+'COLOR'),sg.InputCombo(values=COLORES,default_value=COLORES[0],size=(10,1),key='COL_SUS'),sg.InputCombo(values=COLORES,default_value=COLORES[1],size=(10,1),key='COL_ADJ'),sg.InputCombo(values=COLORES,default_value=COLORES[2],size=(10,1),key='COL_VER')],                 
                    [sg.Text(' '*18+'MINUSCULAS'),sg.InputCombo(values=['MINUSCULAS','MAYUSCULAS'],size=(15,1),key='MINUSCULAS')],
                    [sg.Text(' '*29+'AYUDA'),sg.InputCombo(values=['TOTAL','PARCIAL','DESACTIVADA'],default_value='DESACTIVADA',size=(15,1),key='AYUDA')],
                    [sg.Text(' '*17+'ORIENTACION'),sg.InputCombo(values=['HORIZONTAL','VERTICAL'],size=(15,1),key='ORIENTACION')],
                    [sg.Text(' '*27+'FUENTE'),sg.InputCombo(values=FUENTES,size=(15,1),key='FUENTE')],
                    [sg.Text(' '*27+'OFICINA'),sg.InputCombo(values=list(oficinas.keys()),size=(15,1),key='OFICINAS')],                
                    [sg.Text('\n')],
                    [sg.Button('LISTO',pad=(179,1))]
                ]
config_window = sg.Window('CONFIGURACION', background_color=None).Layout(config_layout)

contador = {'sustantivo':0,'adjetivo':0,'verbo':0 }         #contador de cada tipo
dic = {}                                                    #diccionario que va a almacenar las palabras por tipos 
event , values = config_window.Read()
while event != None:
    if event == 'Agregar':
        ok = False
        palabra = values['PALABRA'].lower()
        if palabra != '' :
            if palabra not in config_window.FindElement('LISTA').GetListValues():
                if bp.buscar(palabra,dic):
                    config_window.FindElement('LISTA').Update(values=list(dic.keys()))
                    contador[dic[palabra]['tipo']] += 1
                    sg.PopupTimed('La palabra '+palabra+' fue ingresada con exito')
                else:
                    sg.PopupError('Ingrese una palabra válida','palabra invalida',keep_on_top=True)
            else:
                sg.Popup('Palabra repetida','La palabra ya fue ingresada... Intente con otra',keep_on_top= True)
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
                ofiAProcesar = values['OFICINAS']
                minusculas = values['MINUSCULAS']
                fuente = values['FUENTE']
                ayuda = values['AYUDA']
                orientacion = values['ORIENTACION']
                colores = [values['COL_SUS'],values['COL_ADJ'],values['COL_VER']]
                config_window.Close()
                sl.jugar(dic,masLarga(dic),ayuda,colores,contador,oficinas,ofiAProcesar,orientacion,fuente,minusculas)
                break
            else:
                sg.PopupError('Ingrese al menos una palabra valida',no_titlebar=True,keep_on_top= True)
    event , values = config_window.Read()
config_window.Close()

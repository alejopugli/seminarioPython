#!/usr/bin/env python36

from pattern.web import Wiktionary as wik
from pattern.es import parse, spelling, lexicon, singularize
import PySimpleGUI as sg
import string
import time

def clasificar(palabra):
    
    clasificaciones = ['NN','VB','VBD','VBG','VBP','VBN','JJ']
    tipo_pattern=''
    
    clasificacion=parse(palabra.lower()).split('/')[1]
        
    if clasificacion == clasificaciones[0]: #sustantivo
        tipo_pattern = 'sustantivo'
    
    elif clasificacion in clasificaciones[1:6]: #verbo
        tipo_pattern = 'verbo'
    
    elif clasificacion == clasificaciones[6]: #adjetivo
        tipo_pattern = 'adjetivo'

    return tipo_pattern

def onPattern(palabra):
    if not palabra in spelling:
        if not palabra in lexicon:
            return False
    return True
    
def parsear_tipo(con):
    tipo=''
    i=0
    while con[i] != ' ':
        tipo += con[i]
        i += 1
    tipo=tipo.lower()
    return tipo

def parsear_descripcion(con):
    i=0
    while con[i] != '1':
        i += 1
    i += 1
    k = i
    while con[k] != '*':
        k += 1
    descripcion = con[i:k-1]
    return descripcion

def esValido(palabra):
	return palabra.lower() in ['adjetivo','sustantivo','verbo']
	
def buscar(palabra,dic):
    engine = wik(language='es')
    articulo = None
    for i in range (0,2): #3 reconexciones, una cada 1 segundos
        try:
            articulo = engine.article(singularize(palabra))
        except:
            time.sleep(0.1)
        else:
            if articulo != None and engine.article(palabra).sections[1].title == 'Español':  #si esta en wiktionary
                                                                        #y es una palabra en español (por que puede encontrar palabras en otro idioma)
                print('Esta en wiktionary')
                try:
                    seccion = articulo.sections[3].content
                    tipo = parsear_tipo(seccion)
                    descripcion = parsear_descripcion(seccion)
                    dic[palabra]={'tipo':tipo,'descripcion':descripcion}
                    ok= True
                except: #si esta en wiktionary pero no pudo parsear la definicion y el tipo...
                    if onPattern(palabra): 
                        tipo = clasificar(singularize(palabra)) #saca el tipo de pattern
                    else:
                        tipo = sg.PopupGetText('Tipo','Ingrese el tipo de la palabra (sustantivo,adjetivo,verbo)').lower() #si no encontro la palabra en pattern se ingresa el tipo manualmente
                        while not esValido(tipo):                                                                     
                            tipo = sg.PopupGetText('Tipo','Ingrese el tipo de la palabra (sustantivo,adjetivo,verbo)').lower()
                            tipo = tipo.lower()
                            dic[palabra]={'tipo':tipo,'descripcion':descripcion}
            elif onPattern(palabra): #si fue None se pureba si esta en pattern
                print('Esta en pattern')
                tipo = clasificar(palabra)
                if tipo != '':
                    descripcion = sg.PopupGetText('Definicion','Ingrese una definicion de la palabra')
                    dic[palabra]={'tipo':tipo,'descripcion':descripcion}
                else:
                    tipo = sg.PopupGetText('Tipo','Ingrese el tipo de la palabra')
                    descripcion = sg.PopupGetText('Definicion','Ingrese una definicion de la palabra')
                    dic[palabra]={'tipo':tipo,'descripcion':descripcion}
            else:
                sg.Popup('Ingrese una palabra válida')
            break
    return dic

        
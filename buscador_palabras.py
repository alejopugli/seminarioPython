#!/usr/bin/env python36

from pattern.web import Wiktionary as wik
from pattern.es import parse, spelling, lexicon, singularize
from datetime import datetime
import PySimpleGUI as sg
import string
import time

def reportar(s):
    '''funcion encargada de abrir el archivo reporte.txt y reportar las palabras que no fueron encontradas'''
    try:
        reporte=open('reporte.txt','a+')
        reporte.write(datetime.now().strftime("%Y-%m-%d %H:%M:%S")+' -- '+s+'\n')
        reporte.close()
    except IOError:
        sg.Popup('Error al escribir en el reporte')

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

    else:
        return ''

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

def esValido(tipo):
	return tipo in ['adjetivo','sustantivo','verbo']

def agregarTipo():
    tipo = sg.PopupGetText('Ingrese el tipo de la palabra','Tipo')
    while True :
        if tipo == None:
            return False
        elif tipo=='':                                                                     
            tipo = sg.PopupGetText('Ingrese el tipo de la palabra (sustantivo,adjetivo,verbo)','Tipo')
        else:
            tipo = tipo.lower()
            if esValido(tipo):
                break
            else:
                tipo = sg.PopupGetText('Tipo','Ingrese un tipo entre (sustantivo,adjetivo,verbo)')
    return tipo

def agregarDescripcion():
    descripcion = sg.PopupGetText('Ingrese la definicion de la palabra','Descripcion') #si no encontro la palabra en pattern se ingresa el tipo manualmente
    while True :
        if descripcion == None:
            return False
        elif descripcion=='':                                                                     
            descripcion = sg.PopupGetText('Ingrese la definicion de la palabra','Descripcion')
        else:
            break
    return descripcion
    	
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
                try:
                    seccion = articulo.sections[3].content
                    tipo = parsear_tipo(seccion)
                    descripcion = parsear_descripcion(seccion)
                    dic[palabra]={'tipo':tipo,'descripcion':descripcion}
                    reportar(palabra + ' está en wiktionary')
                    return dic
                except: #si esta en wiktionary pero no pudo parsear la definicion y el tipo...
                    if onPattern(palabra): 
                        tipo = clasificar(singularize(palabra)) #saca el tipo de pattern
                        if not esValido(tipo):
                            tipo = agregarTipo()
                            if not tipo:
                                return False
                        descripcion = agregarDescripcion()
                        if not descripcion:
                            return False
                        dic[palabra]={'tipo':tipo,'descripcion':descripcion}
                        reportar(palabra + ' está en pattern')
                        return dic
                    else:
                        tipo = agregarTipo()
                        if not tipo:
                            return False
                        descripcion = agregarDescripcion()
                        if not descripcion:
                            return False
                        dic[palabra]={'tipo':tipo,'descripcion':descripcion}
                        reportar(palabra + ' no está ni en wiktionary o pattern')
                        return dic
            elif onPattern(palabra): #si fue None se pureba si esta en pattern
                tipo = clasificar(palabra)
                if not esValido(tipo):
                    tipo = agregarTipo()
                    if not tipo:
                        return False
                descripcion = agregarDescripcion()
                if not descripcion:
                    return False
                reportar(palabra + ' con tipo y descripcion generada por el usuario')
                dic[palabra]={'tipo':tipo,'descripcion':descripcion}
                return dic
            else:
                reportar(palabra + ' no esta en wiktionary ni en pattern')
                sg.Popup('Ingrese una palabra válida')
                return False
        
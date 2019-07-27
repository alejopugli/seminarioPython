#!/usr/bin/env python36

from pattern.web import Wiktionary as wik
from pattern.es import parse, spelling, lexicon, singularize
import string

def parsear_tipo(con):
    tipo=''
    i=0
    while con[i] != ' ':
        tipo += con[i]
        i += 1
    tipo=tipo.lower()
    return tipo

def parsear_descripcion(con):
    tipo=''
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
	if palabra.lower() not in ['adjetivo','sustantivo','verbo']:
		return False
	else:
		return True

def buscar(palabra,dic,contador):
    ok = False #indica si la palabra se va a agregar a la lista o no
    articulo = None
    for i in range (0,2): #3 reconexciones, una cada 1 segundos
        try:
            articulo = engine.article(singularize(palabra))
        except:
            time.sleep(1)
        else:
            if engine.article(palabra).sections[1].title == 'Español':  #si esta en wiktionary
                                                                        #y es una palabra en español (por que puede encontrar palabras en otro idioma)
                print('Esta en wiktionary')
                try:
                    seccion = articulo.sections[3].content
                    tipo = parsear_tipo(seccion)
                    descripcion = parsear_descripcion(seccion)
                except: #si esta en wiktionary pero no pudo parsear la definicion y el tipo...
                    if onPattern(palabra): 
                        tipo = clasificar(singularize(palabra)) #saca el tipo de pattern
                    else:
                        tipo = sg.PopupGetText('Tipo','Ingrese el tipo de la palabra (sustantivo,adjetivo,verbo)').lower() #si no encontro la palabra en pattern se ingresa el tipo manualmente
                        while not esValido(tipo):                                                                     
                            tipo = sg.PopupGetText('Tipo','Ingrese el tipo de la palabra (sustantivo,adjetivo,verbo)').lower()
                            tipo = tipo.lower()
            elif onPattern(palabra): #si fue None se pureba si esta en pattern
                print('Esta en pattern')
                tipo = clasificar(palabra)
                print(tipo,'entro por pattern')
                if tipo != '':
                    descripcion = sg.PopupGetText('Definicion','Ingrese una definicion de la palabra')
                    ok = True
            else:
                sg.Popup('La palabra ya existe, ingrese otra')
            break
    return ok

        
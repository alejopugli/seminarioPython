#!/usr/bin/env python36

import sys
import PySimpleGUI as sg
import random
from pattern.web import Wiktionary as wik
from pattern.es import parse, spelling, lexicon, singularize
import string
from datetime import datetime
import time


"""
MIEMBROS DEL GRUPO:
CRIS, SEBASTIAN AGUSTIN
PUGLIESE, ALEJO EZEQUIEL
PISONI, FELIPE
"""

BOX_SIZE = 25 #constante que representa el tamaño de un "casillero"
COLORES = ['ROJO','VERDE','AZUL','AMARILLO','ROSA','VIOLETA']
CANTIDAD = list(range(0,6))
FUENTES = [ 'Arial' ,'Courier', 'Comic', 'Fixedsys','Times','Verdana','Helvetica' ]


def tipoAyuda(ayuda, contador, ayudas, dic):
    if ayuda != 'TOTAL':
        sopa_window.FindElement('PALABRAS').Update(visible=False)
        
    if ayuda == 'TOTAL':
        sopa_window.FindElement('PALABRAS').Update(values=list(dic.keys()))
    elif ayuda =='PARCIAL':
        sopa_window.FindElement('HELP').Update(visible=True)
        for i in dic.keys():
            descripcion = dic[i]['descripcion']
            ayudas.append(descripcion)
    else:
        cadena='SUSTANTIVOS:'+str(contador['sustantivo'])+'  ADJETIVOS:'+str(contador['adjetivo'])+'  VERBOS:'+str(contador['verbo'])
        sopa_window.FindElement('CANTIDAD').Update(value=cadena, visible=True)


def esValido(palabra):
	if palabra.lower() not in ['adjetivo','sustantivo','verbo']:
		return False
	else:
		return True


def masLarga(dic):
    sortedwords = sorted(dic.keys(), key=len, reverse=True)
    return len(sortedwords[0])


def reportar(s):
    try:
        reporte=open('reporte.txt','a+')
        reporte.write(datetime.now().strftime("%Y-%m-%d %H:%M:%S")+' -- '+s+'\n')
        reporte.close()
    except IOError:
        sg.Popup('No se pudo escribir en el reporte')



def cumple(c_sus,c_adj,c_ver,con):
    sus=False
    adj=False
    ver=False
    if con['sustantivo'] == c_sus:
        sus=True

    if con['adjetivo'] == c_adj:
        adj=True

    if con['verbo'] == c_ver:
        ver=True

    if sus and adj and ver:
        return True
    
    elif not sus:
        if c_sus-con['sustantivo'] > 0:
            sg.Popup('Faltan '+str(c_sus-con['sustantivo'])+' sustantivos')
        else:
            sg.Popup('Sobran '+str((c_sus-con['sustantivo'])*-1)+' sustantivos')
        return False
    elif not adj:
        if c_adj-con['adjetivo'] > 0:
            sg.Popup('Faltan '+str(c_adj-con['adjetivo'])+' adjetivos')
        else:
            sg.Popup('Sobran '+str((c_adj-con['adjetivo'])*-1)+' adjetivos')
        return False
    elif not ver:
        if c_ver-con['verbo'] > 0:
            sg.Popup('Faltan '+str(c_ver-con['verbo'])+' verbos')
        else:
            sg.Popup('Sobran '+str((c_ver-con['verbo'])*-1)+' verbos')
        return False
        
        

def onPattern(palabra):
    if not palabra in spelling:
        if not palabra in lexicon:
            return False
        else:
            return True
    else:
        return True

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


#ventana de la sopa de letras:
sopa_layout = [
                [sg.Text('',visible=False,size=(50,1),font='Courier 20',key='CANTIDAD')],
                [sg.Button('AYUDA',key='HELP',visible=False)],
                [sg.Graph((800,800), (0,450), (450,0), key='_GRAPH_', change_submits=True, drag_submits=True),
                 sg.Listbox(values=[],size=(100,10),key='PALABRAS',font='Comic 18',visible=True)]
              ]
sopa_window = sg.Window('SOPA DE LETRAS', resizable=True).Layout(sopa_layout).Finalize()
sopa_window.Disappear()



#ventana configuracion:
config_layout = [
                   [sg.Text('PALABRAS'),sg.Input(size=(35,1),key='PALABRA'),sg.Button('Agregar',bind_return_key=True)],
                   [sg.Listbox(values=[],size=(55,6),key='LISTA',select_mode="LISTBOX_SELECT_MODE_single", bind_return_key=True)],
                   [sg.Button('Eliminar')],
                   [sg.Text('\n')],
                   [sg.Text(' '*19+'SUSTANTIVOS'+' '*2),sg.Text('ADJETIVOS'+' '*6),sg.Text('VERBOS')],
                   [sg.Text('CANTIDAD'),sg.InputCombo(values=CANTIDAD,default_value=CANTIDAD[1],size=(10,1),key='SUSTANTIVOS'),sg.InputCombo(values=CANTIDAD,default_value=CANTIDAD[1],size=(10,1),key='ADJETIVOS'),sg.InputCombo(values=CANTIDAD,default_value=CANTIDAD[1],size=(10,1),key='VERBOS')],
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

def decidir(i,filas,lista,palabra,dispersion):
    if random.choice(dispersion) and len(lista) > 0:
        if len(palabra) <= filas - i:
            print (filas - i)
            return True
        else:
            return False
    else:
        return False
    
    

def generar_sopa(dic,longitud, orientacion='HORIZONTAL',fuente='Comic',minusculas=False):

    lista = list(dic.keys())

    dispersion = [True]
    m = lambda l: 1 if l >= 8 else -2
    
    for j in range(longitud-m(longitud)):
        dispersion.append(False)
    print(dispersion)
    
    '''
    "dispersion" es la probabilidad de que de positiva la decision de poner
    una palabra en una fila. Notar que mientras mas False haya menor la probabilidad
    de poner una palabra en cierta linea, por lo cual la dispersion de las palabras
    tiende a ser mayor. La cantidad de Flase esta determinada por el tamaño de la grilla.
    En las pruebas realizadas longitud-1 de "Falses" fue un numero que permitio una dispersion
    aceptable sin que queden palabras afuera cuando la matriz era de 16*16 o mayor, mientras que
    cuando la matriz era mas chica para que la dispersion sea mas grande se requieren mas Falses
    por lo que longitud-(-2) = longitud + 2 dio resultados de dispersion aceptables
    '''

    filas = longitud * 2
    
    if minusculas:
        mayus_minus=string.ascii_lowercase
    else:
        mayus_minus=string.ascii_uppercase
        lista = [x.upper() for x in lista]

    matriz = [ ]

    for i in range(filas):
        row = [ ]
        k=0
        while k < filas:
            if len(lista) > 0 :
                palabra = random.choice(lista)
            if decidir(k,filas,lista,palabra,dispersion):
                lista.remove(palabra)
                n = 0
                while k < filas and n < len(palabra):
                    row.append(palabra[n])
                    n += 1
                    k += 1
            else:
                row.append(random.choice(mayus_minus))
                k += 1
        
        matriz.append(row)
        

    print(matriz)
    dibujar_sopa(matriz,masLarga(dic),fuente)

    return matriz






def dibujar_sopa(matriz, longitud, fuente='Comic'):
    
    g = sopa_window.FindElement('_GRAPH_')
    
    filas = longitud*2
    columnas = filas #matriz cuadrada

        
    for row in range(filas):
    
        for col in range(columnas):
                g.DrawRectangle((col * BOX_SIZE + 5, row * BOX_SIZE + 3), (col * BOX_SIZE + BOX_SIZE + 5, row * BOX_SIZE + BOX_SIZE + 3), line_color='black') #se dibuja cuadrado
                box_x = (col * BOX_SIZE + 5) // BOX_SIZE
                box_y = (row * BOX_SIZE + 3) // BOX_SIZE
                letter_location = (box_x * BOX_SIZE + 18, box_y * BOX_SIZE + 17)
                g.DrawText('{}'.format(matriz[row][col]), letter_location, font=fuente+' '+str(BOX_SIZE)) 



def main(argv):

    
    engine=wik(language='es')

    dic_colores = {'ROJO':'red','AMARILLO':'yellow','VERDE':'green','AZUL':'blue','ROSA':'pink','VIOLETA':'purple'}

    config_window = sg.Window('CONFIGURACION', background_color=None).Layout(config_layout)
    dic = {}
    palabras = [ ]

    contador = {'sustantivo':0,'adjetivo':0,'verbo':0 }
    
    while True:
        event, values = config_window.Read()
        if event is None:
            sys.exit()
            
        elif event == 'Agregar': #se agrega palabra

            ok = False #indica si la palabra se va a agregar a la lista o no
            palabra = values['PALABRA'].lower()
            articulo = None
            for i in range (0,3): #3 reconexciones, una cada 5 segundos
                try:
                    articulo = engine.article(singularize(palabra))
                    break
                except:
                    time.sleep(5)
            
                
            #if len(palabra)>      

            if palabra not in config_window.FindElement('LISTA').GetListValues():
                
            
                if articulo != None and  engine.article(palabra).sections[1].title == 'Español': #si no es None esta en wiktionary
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
                            
                        if tipo != '':   #parche para palabras que califican en pattern como UH que serian interjecciones como 'hola' u 'oh', y otros tipos que no nos competen
                          descripcion = sg.PopupGetText('Definicion',)
                    
                    if onPattern(palabra):
                        
                        tipo_pattern = clasificar(palabra)    
                    
                        if tipo_pattern != tipo:
                            print('no match')
                            reportar(palabra + ' no coincide en pattern y wiktionary')

                    if tipo in ['sustantivo','adjetivo','verbo']:
                        ok = True

                    print(tipo,' entro por wik')

                elif onPattern(palabra): #si fue None se pureba si esta en pattern
                    print('Esta en pattern')
                    tipo = clasificar(palabra)
                    print(tipo,'entro por pattern')
                    if tipo != '':
                        descripcion = sg.PopupGetText('Definicion','Ingrese una definicion de la palabra')
                        ok = True

                if ok: #Estaba en pattern o wiktionary entonces se agrega
                    palabras.append(palabra)
                    config_window.FindElement('LISTA').Update(values=palabras)
                    dic[palabra]={'tipo':tipo,'descripcion':descripcion}
                    contador[tipo] += 1
                else: #no estaba en ningun lado y no se agrega
                    sg.Popup("""No se pudo agregar la palabra, puede que:\n
                    *la palabra no existe\n
                    *la palabra esta mal escrita\n
                    *la palabra no es un sustantivo\n
                    *la palabra no es un adjetivo\n
                    *la palabra no es un verbo """)
                    reportar(palabra + ' no esta en wiktionary ni en pattern')
            else:
                sg.Popup('La palabra ya existe, ingrese otra')





        elif event == 'LISTA': #si se hace doble clcik en un elemento de la lista se muestra la definicion de la palabra
            sg.Popup('Definicion',dic[values['LISTA'][0]]['descripcion'])


            
        elif event == 'Eliminar':
            if len(list(dic.keys())) > 0:
                contador[ dic[values['LISTA'][0]] ['tipo'] ] -= 1
                del dic[values['LISTA'][0]]
                config_window.FindElement('LISTA').Update(values=list(dic.keys()))



        elif event == 'LISTO':

            ##ASIGNACIONES##
            c_sustantivos = int(values['SUSTANTIVOS']) #cantidad sustantivos,adjetivos,verbos
            c_adjetivos = int(values['ADJETIVOS'])
            c_verbos = int(values['VERBOS'])

            if cumple(c_sustantivos,c_adjetivos,c_verbos,contador):
                col_sus = dic_colores[values['COL_SUS']]
                col_adj = dic_colores[values['COL_ADJ']]
                col_ver = dic_colores[values['COL_VER']]
                ayuda = values['AYUDA']
                minusculas = values['MINUSCULAS']
                fuente = values['FUENTE']
                orientacion = values['ORIENTACION']
                longitud = masLarga(dic)
                matriz = generar_sopa(dic,longitud,orientacion,fuente,minusculas)
                break
        
    config_window.Close()
    
    sopa_window.Reappear()


    ayudas = [ ]
    tipoAyuda(ayuda,contador,ayudas,dic)
    g = sopa_window.FindElement('_GRAPH_')

    boxX_ant = None
    boxY_ant = None
    Borrar=True
    while True:
        event, values = sopa_window.Read()
        print(event, values)
        if event is None:
            break
        mouse = values['_GRAPH_']
        time.sleep(0.6)
        if event == '_GRAPH_':
            if mouse == (None, None):
                continue
            box_x = mouse[0]//BOX_SIZE
            box_y = mouse[1]//BOX_SIZE
            palabra=''
            letter_location = (box_x * BOX_SIZE + 18, box_y * BOX_SIZE + 17)
            print(box_x, box_y)
            if boxX_ant == None and boxY_ant == None:
                print('entre primer if')
                g.DrawText('{}'.format(matriz[box_y][box_x]), letter_location,color="grey", font=fuente+' '+str(BOX_SIZE))
                boxY_ant = box_y
                boxX_ant = box_x
            elif box_y == boxY_ant and box_x != boxX_ant:
                try:
                    print('entre segundo if')
                    if( box_x > boxX_ant):
                        for i in range(boxX_ant, box_x+1):
                            letra = matriz[box_y][i]
                            palabra += letra.lower()
                            print(palabra)
                        atras = False
                    else:
                        for i in reversed(range(box_x, boxX_ant+1)):
                            letra = matriz[box_y][i]
                            palabra += letra.lower()
                            print(palabra)
                        palabra = palabra[::-1]
                        atras = True
                        print(palabra)
                    if palabra in dic.keys():
                        tipo = dic[palabra]['tipo']
                        if tipo == 'sustantivo':
                            color = col_sus
                            c_sustantivos-=1
                        elif tipo == 'adjetivo':
                            color = col_adj
                            c_adjetivos-=1
                        elif tipo == 'verbo':
                            color = col_ver
                            c_verbos-=1
                    else:
                        color = 'black'
                    if (atras):
                        for i in range(box_x, boxX_ant+1):
                            letter_location = (i * BOX_SIZE + 18, box_y * BOX_SIZE + 17)
                            g.DrawText('{}'.format(matriz[box_y][i]), letter_location,color=color, font=fuente+' '+str(BOX_SIZE))
                    else:
                        for i in range(boxX_ant, box_x+1):
                            letter_location = (i * BOX_SIZE + 18, box_y * BOX_SIZE + 17)
                            g.DrawText('{}'.format(matriz[box_y][i]), letter_location,color=color, font=fuente+' '+str(BOX_SIZE))
                    boxY_ant = box_y
                    boxX_ant = box_x
                    Borrar = False
                except:
                    pass
            else:
                print('entre tercer if')
                letter_location_ant= (boxX_ant * BOX_SIZE + 18, boxY_ant * BOX_SIZE + 17)
                try:
                    if (Borrar) :
                        g.DrawText('{}'.format(matriz[boxY_ant][boxX_ant]), letter_location_ant,color="black", font=fuente+' '+str(BOX_SIZE))                    
                    g.DrawText('{}'.format(matriz[box_y][box_x]), letter_location,color="grey", font=fuente+' '+str(BOX_SIZE))
                except:
                    pass
                boxY_ant = box_y
                boxX_ant = box_x
                Borrar=True
        victoria = (c_sustantivos < 1 and c_adjetivos < 1 and c_verbos < 1)
        if(victoria):
            sg.Popup('Ganaste!')
            break
        if event == 'HELP':
            descripcion = random.choice(ayudas)
            sg.Popup('Ayuda',descripcion)
    sopa_window.Close()


if __name__ == "__main__":
    main(sys.argv[1:])

import PySimpleGUI as sg
import random
import string

BOX_SIZE = 25 #constante que representa el tamaño de un "casillero"

dic_colores = {'ROJO': 'red', 'AMARILLO':'yellow','VERDE':'green','AZUL':'blue','ROSA':'pink','VIOLETA':'purple'}

def decidir(i,filas,lista,palabra,dispersion):
    if random.choice(dispersion) and len(lista) > 0:
        if len(palabra) <= filas - i:
            return True
    return False
   
def rotar(matriz):
    '''Esta función permite rotar la matriz de manera que las palabras se muestren verticalmente'''
    return list(zip(*matriz[::-1]))

def generar_sopa(dic,longitud,orientacion='HORIZONTAL',minusculas='MAYUSCULAS'):
    '''funcion responsable de generar la matriz de letras aleatorias con las palabras definidas'''
    lista = list(dic.keys())
    dispersion = [True]
    m = lambda l: 1 if l >= 8 else -2 
    #for j in range(longitud-valor(longitud,len(lista))):
    for j in range(longitud - m(longitud)):
        dispersion.append(False)
    filas = longitud * 2
    if (minusculas == 'MINUSCULAS'):
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
    if (orientacion == 'VERTICAL'):
        matriz = rotar(matriz)
    return matriz

def dibujar_sopa(matriz, g, longitud, fuente='Comic'):
    '''funcion que dibuja la sopa de letras con la matriz previamente generada'''
    filas = longitud*2
    columnas = filas #matriz cuadrada
    for row in range(filas):
        for col in range(columnas):
            g.DrawRectangle((col * BOX_SIZE + 5, row * BOX_SIZE + 3), (col * BOX_SIZE + BOX_SIZE + 5, row * BOX_SIZE + BOX_SIZE + 3), line_color='black') #se dibuja cuadrado
            box_x = (col * BOX_SIZE + 5) // BOX_SIZE
            box_y = (row * BOX_SIZE + 3) // BOX_SIZE
            letter_location = (box_x * BOX_SIZE + 18, box_y * BOX_SIZE + 17)
            g.DrawText('{}'.format(matriz[row][col]), letter_location, font=fuente+' '+str(BOX_SIZE)) 

def color_a_pintar(tipo,colores):
    '''esta funcion devuelve el color correspondiente segun el tipo de palabra ingresado'''
    if tipo == 'sustantivo':
        return dic_colores[colores[0]]
    elif tipo == 'adjetivo':
        return dic_colores[colores[1]]
    else:
        return dic_colores[colores[2]]

def pintar(matriz,x_y,anterior,g,fuente,color='black'):
    '''esta funcion es la encargada de pintar la palabra seleccionada y devuelve la misma'''
    palabra = '' 
    if anterior[0] == x_y[0]:
        if anterior[1]< x_y[1]:
            rango = range(anterior[1], x_y[1]+1)
        else:
            rango = range( x_y[1],anterior[1]+1)
    else:
        if anterior[0]<x_y[0]:
            rango = range(anterior[0], x_y[0]+1)
        else:
            rango = range(x_y[0],anterior[0]+1)
    for i in rango:
        if anterior[0] == x_y[0]:
            letra = matriz[i][x_y[0]]
            palabra += letra.lower()
            letter_location = (x_y[0] * BOX_SIZE + 18, i * BOX_SIZE + 17)
            try:
                g.DrawText('{}'.format(matriz[i][x_y[0]]), letter_location, color=color, font=fuente+' '+str(BOX_SIZE))
            except:
                pass
        else:
            letra = matriz[x_y[1]][i]
            palabra += letra.lower()
            letter_location = (i * BOX_SIZE + 18, x_y[1] * BOX_SIZE + 17)
            try:
                g.DrawText('{}'.format(matriz[x_y[1]][i]), letter_location, color=color, font=fuente+' '+str(BOX_SIZE))
            except:
                pass
    return palabra
    

def jugar(dic , longitud ,colores, cantidades, orientacion, fuente, minusculas):
    '''funcion principal encargada de operar en la sopa de letras'''
    matriz = generar_sopa(dic, longitud, orientacion, minusculas)
    sopa_layout = [
            [sg.Text('',visible=False,size=(30,1),font='Courier 20',key='CANTIDAD')],
            [sg.Button('AYUDA',key='HELP',visible=True)],
            [sg.Text('TIPO'),sg.InputCombo(values=['sustantivo','adjetivo','verbo'],size=(15,1),key='TIPO')],
            [sg.Button('SALIR',key='EXIT',visible=False)],
            [sg.Graph((800,800), (0,450), (450,0), key='_GRAPH_', change_submits=True, drag_submits=False)],
            ]

            
    sopa_window = sg.Window('SOPA DE LETRAS', resizable=True).Layout(sopa_layout).Finalize()
    g = sopa_window.FindElement('_GRAPH_')
    
    dibujar_sopa(matriz, g, longitud, fuente)
    anterior=()
    palabra=''
    event, values = sopa_window.Read()
    tipo = values['TIPO'] #variable utilizada para saber el tipo de palabra que va a buscar
    color = color_a_pintar(tipo,colores)
    while event != None:
        if event == 'HELP':
            #Agregar distintas ayudas
            sg.Popup('Buscá la palabra: ', random.choice(list(dic.keys())))
        elif event == 'TIPO':
            tipo = values
            color = color_a_pintar(tipo,colores)
        elif event == '_GRAPH_':
            mouse = values['_GRAPH_']
            if mouse == (None,None):
                event, values = sopa_window.Read()
                continue
            else:
                x_y = (mouse[0]//BOX_SIZE, mouse[1]//BOX_SIZE)
            #pinto la primera letra
            letter_location = (x_y[0]* BOX_SIZE + 18, x_y[1] * BOX_SIZE + 17)
            try:
                g.DrawText('{}'.format(matriz[x_y[1]][x_y[0]]),letter_location,color=color, font=fuente+' '+str(BOX_SIZE))
            except:
                pass
            if palabra == '':
                #cuando no tengo seleccion previa, agrego la primera letra
                letra = matriz[x_y[1]][x_y[0]]
                palabra += letra.lower()
            else:
                if x_y[0] != anterior[0] and x_y[1] != anterior[1]:
                    #solo entra cuando la 2da seleccion es en diagonal
                    letter_location = (anterior[0]* BOX_SIZE + 18, anterior[1] * BOX_SIZE + 17)
                    try:
                        #pinto la anterior en negro
                        g.DrawText('{}'.format(matriz[anterior[1]][anterior[0]]),letter_location,color='black', font=fuente+' '+str(BOX_SIZE))
                    except:
                        pass                                      
                    letter_location = (x_y[0]* BOX_SIZE + 18, x_y[1] * BOX_SIZE + 17)
                    try:
                        #pinto la nueva letra del color (segun el tipo)
                        g.DrawText('{}'.format(matriz[x_y[1]][x_y[0]]),letter_location,color=color, font=fuente+' '+str(BOX_SIZE))
                    except:
                        pass
                else:
                    palabra = pintar(matriz,x_y,anterior,g,fuente,color)
                    if palabra in list(dic.keys()):
                        if dic[[palabra][0]]['tipo']!=tipo:
                            sg.Popup('¡Muy Bien! Encontraste una palabra,\npero no es un: '+tipo)
                            pintar(matriz,x_y,anterior,g,fuente)
                        else:
                            del dic[[palabra][0]]
                            if len(dic.keys()) > 0 :
                                sg.Popup('¡Felicitaciones! Haz encontrado una palabra,\nsolo faltan '+ str(len(dic.keys())))
                            else:
                                sg.Popup('¡Felicitaciones! Haz encontrado la ultima palabra!\n¡Haz Ganado!')
                                sopa_window.FindElement('EXIT').Update(visible=True)
                                while event != 'EXIT':
                                    event, values = sopa_window.Read()
                                break
                    else :
                        pintar(matriz,x_y,anterior,g,fuente) #vuelvo a pintar pero en negro
                        sg.Popup('Ups, esa no es una palabra válida')
                    palabra = ''
            anterior = x_y
        event, values = sopa_window.Read()
    sopa_window.Close()

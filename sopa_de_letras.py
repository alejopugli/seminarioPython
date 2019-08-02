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

def generar_sopa(dic,longitud, colores,cantidades, orientacion='HORIZONTAL',fuente='Comic',minusculas='MAYUSCULAS'):
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
        
def jugar(dic , longitud ,colores, cantidades, orientacion, fuente, minusculas):
    
    matriz = generar_sopa(dic, longitud, colores, cantidades, orientacion, fuente, minusculas)
    
    sopa_layout = [
            [sg.Text('',visible=False,size=(30,1),font='Courier 20',key='CANTIDAD')],
            [sg.Button('AYUDA',key='HELP',visible=True)],
            [sg.Text('TIPO'),sg.InputCombo(values=['sustantivo','adjetivo','verbo'],size=(15,1),key='TIPO')],
            [sg.Graph((600,600), (0,450), (450,0), key='_GRAPH_', change_submits=True, drag_submits=False)],
            ]
            
    sopa_window = sg.Window('SOPA DE LETRAS', resizable=True).Layout(sopa_layout).Finalize()
    g = sopa_window.FindElement('_GRAPH_')
    
    dibujar_sopa(matriz, g, longitud, fuente)
    palabra=''
    anterior=()
    while True:
        event, values = sopa_window.Read()
        tipo = values['TIPO'] #variable utilizada para saber el tipo de palabra que va a buscar
        color = color_a_pintar(tipo,colores)
        if event == 'HELP':
            #Agregar distintas ayudas
            sg.Popup('Buscá la palabra: ', random.choice(list(dic.keys())))
        elif event == 'TIPO':
            tipo = values
        elif event == '_GRAPH_':
            mouse = values['_GRAPH_']
            print(mouse, ' mouse')
            if mouse == (None,None):
                continue
            else:
                if (orientacion == 'VERTICAL'):
                    x_y = (mouse[1]//BOX_SIZE, mouse[0]//BOX_SIZE)
                else:
                    x_y = (mouse[0]//BOX_SIZE, mouse[1]//BOX_SIZE)
            print(x_y, ' x_y')
            print(anterior, ' anterior')
            
            if anterior == ():
                letter_location = (x_y[0]* BOX_SIZE + 18, x_y[1] * BOX_SIZE + 17)
                print(letter_location)
                print("anterior = null")
                try:
                    g.DrawText('{}'.format(matriz[x_y[1]][x_y[0]]),letter_location,color=color, font=fuente+' '+str(BOX_SIZE))
                except:
                    pass
            else:
                print(anterior,' anterior')
                atras = False
                if x_y[1] >= anterior[1] :
                    print('x_y es mayor')
                    for i in range(anterior[0], x_y[0]+1):
                        letra = matriz[x_y[1]][i]
                        palabra += letra.lower()
                    print(palabra)
                    atras = False
                elif x_y[1] < anterior[1] :
                    print('x_y es menor')
                    for i in reversed(range(anterior[1], x_y[1]+1)):
                        letra = matriz[x_y[1]][i]
                        palabra += letra.lower()
                    palabra = palabra[::-1]
                    atras = True
                    print(palabra)
                if (atras):
                    for i in range(x_y[1], anterior[1]+1):
                        letter_location = (i * BOX_SIZE + 18, x_y[1] * BOX_SIZE + 17)
                        try:
                            g.DrawText('{}'.format(matriz[x_y[1]][i]), letter_location, color=color, font=fuente+' '+str(BOX_SIZE))
                        except:
                            pass
                else:
                    for i in range(anterior[0], x_y[0]+1):
                        letter_location = (i * BOX_SIZE + 18, x_y[1] * BOX_SIZE + 17)
                        try:
                            g.DrawText('{}'.format(matriz[x_y[1]][i]), letter_location, color=color, font=fuente+' '+str(BOX_SIZE))
                        except:
                            pass
                if palabra in list(dic.keys()):
                    print(dic[[palabra][0]]['tipo'])
                    print(tipo)
                    if dic[[palabra][0]]['tipo']!=tipo:
                        sg.Popup('¡Muy Bien! Encontraste una palabra, \n pero no es un: '+tipo)
                    else:
                        del dic[[palabra][0]]
                        sg.Popup('¡Felicitaciones! Haz encontrado una palabra, \n solo faltan: '+ str(len(dic.keys())))
                else:
                    sg.Popup('Ups, esa no es una palabra válida')
        else:
            break
        anterior = x_y
        if(len(dic.keys())==0):
            sg.Popup('Ganaste!')
            break
    sopa_window.Close()

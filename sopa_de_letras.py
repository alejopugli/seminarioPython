import PySimpleGUI as sg
import random
import string

BOX_SIZE = 25 #constante que representa el tamaño de un "casillero"
sopa_layout = [
            [sg.Text('',visible=False,size=(50,1),font='Courier 20',key='CANTIDAD')],
            [sg.Button('AYUDA',key='HELP',visible=False)],
            [sg.Graph((800,800), (0,450), (450,0), key='_GRAPH_', change_submits=True, drag_submits=False),
            sg.Listbox(values=[],size=(100,10),key='PALABRAS',font='Comic 18',visible=True)]
            ]
dic_colores = {'ROJO': 'red', 'AMARILLO':'yellow','VERDE':'green','AZUL':'blue','ROSA':'pink','VIOLETA':'purple'}

def jugar(sopa_window , matriz , fuente , dic ,colores, cantidades ):
    g = sopa_window.FindElement('_GRAPH_')
    col_sus = dic_colores[colores[0]]
    col_adj = dic_colores[colores[1]]
    col_ver = dic_colores[colores[2]]
    boxX_ant = None
    boxY_ant = None
    Borrar=True
    while True:
        event, values = sopa_window.Read()
        print(event, values)
        if event is None:
            break
        mouse = values['_GRAPH_']
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
                            cantidades[0]-=1
                        elif tipo == 'adjetivo':
                            color = col_adj
                            cantidades[1]-=1
                        elif tipo == 'verbo':
                            color = col_ver
                            cantidades[2]-=1
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
        victoria = (cantidades[0] < 1 and cantidades[1] < 1 and cantidades[2] < 1)
        if(victoria):
            sg.Popup('Ganaste!')
            break
        if event == 'HELP':
            descripcion = random.choice(ayudas)
            sg.Popup('Ayuda',descripcion)
    sopa_window.Close()

    
    
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

def decidir(i,filas,lista,palabra,dispersion):
    if random.choice(dispersion) and len(lista) > 0:
        if len(palabra) <= filas - i:
            return True
    return False
   

ayudas = [ ]
def generar_sopa(dic,longitud, colores,cantidades, orientacion='HORIZONTAL',fuente='Comic',minusculas=False):

    lista = list(dic.keys())

    dispersion = [True]
    m = lambda l: 1 if l >= 8 else -2
    
    #for j in range(longitud-valor(longitud,len(lista))):
    for j in range(longitud - m(longitud)):
        dispersion.append(False)
    
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
        
    dibujar_sopa(matriz,longitud,dic,colores,cantidades,fuente,minusculas)

def dibujar_sopa(matriz, longitud, dic, colores, cantidades, fuente='Comic',minusculas=False):
    sopa_window = sg.Window('SOPA DE LETRAS', resizable=True).Layout(sopa_layout).Finalize()
    
    g = sopa_window.FindElement('_GRAPH_')
    
    filas = longitud*2
    columnas = filas #matriz cuadrada
   
    for row in range(filas):
    
        for col in range(columnas):
                g.DrawRectangle((col * BOX_SIZE + 5, row * BOX_SIZE + 3), (col * BOX_SIZE + BOX_SIZE + 5, row * BOX_SIZE + BOX_SIZE + 3), line_color='black') #se dibuja cuadrado
                box_x = (col * BOX_SIZE + 5) // BOX_SIZE
                box_y = (row * BOX_SIZE + 3) // BOX_SIZE
                letter_location = (box_x * BOX_SIZE + 18, box_y * BOX_SIZE + 17)
                g.DrawText('{}'.format(matriz[row][col]), letter_location)#, font=fuente+' '+str(BOX_SIZE)) 
    jugar(sopa_window, matriz , fuente , dic , colores , cantidades)


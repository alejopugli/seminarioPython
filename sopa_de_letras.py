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

def color_a_pintar(tipo,colores)
	'''esta funcion devuelve el color correspondiente segun el tipo de palabra ingresado'''
	if tipo == 'SUSTANTIVO':
		return dic_colores[colores[0]]
	elif tipo == 'ADJETIVO':
		return dic_colores[colores[1]]
	else:
		return dic_colores[colores[2]]
def jugar(dic , longitud ,colores, cantidades, orientacion, fuente, minusculas):
    
    matriz = generar_sopa(dic, longitud, colores, cantidades, orientacion, fuente, minusculas)
    
    sopa_layout = [
            [sg.Text('',visible=False,size=(30,1),font='Courier 20',key='CANTIDAD')],
            [sg.Button('AYUDA',key='HELP',visible=True)],
            [sg.Graph((800,800), (0,450), (450,0), key='_GRAPH_', change_submits=True, drag_submits=False)],
            [sg.Text('TIPO'),sg.InputCombo(values=['SUSTANTIVO','ADJETIVO','VERBO'],size=(15,1),key='TIPO')],
            [sg.Listbox(values=list(dic.keys()),size=(10,10),key='PALABRAS',font='Comic 18',visible=True)]
            ]
            
    sopa_window = sg.Window('SOPA DE LETRAS', resizable=True).Layout(sopa_layout).Finalize()
    g = sopa_window.FindElement('_GRAPH_')
    
    dibujar_sopa(matriz, g, longitud, fuente)
   
	tipo = sopa_window.FindElement('TIPO') #variable utilizada para saber el tipo de palabra que va a buscar
    
    event, values = sopa_window.Read()
    anterior=(,)
    while event != None:
    	color = color_a_pintar(tipo,colores)
        if event == 'HELP'
        	#Agregar ayudas
        	sg.Popup('Buscá la palabra: ', random.choice(dic.keys()))
        elif event == 'TIPO':
        	tipo = values
        elif event == '_GRAPH_':
            mouse = values['_GRAPH_']
            if (orientacion == 'VERTICAL')
            	x_y = (mouse[1]//BOX_SIZE, mouse[0]//BOX_SIZE)
            else:
            	x_y = (mouse[0]//BOX_SIZE, mouse[1]//BOX_SIZE)
            if mouse == (None, None):
                pass
            elif anterior == (None,None):
            	g.DrawText('{}'.format(matriz[box_y][box_x]), letter_location,color="grey", font=fuente+' '+str(BOX_SIZE))
            	anterior = x_y
            elif anterior != x_y
           		if x_y[0] > anterior[0]
					for i in range(anterior[0], x_y[0]+1):
                       	letra = matriz[x_y[0]][i]
                       	palabra += letra.lower()
                       	print(palabra)
                	atras = False
                else:
                	for i in reversed(range(x, x_y[0]+1)):
                    	letra = matriz[x_y[0]][i]
                        palabra += letra.lower()
                        print(palabra)
                    palabra = palabra[::-1]
                    atras = True
                    print(palabra)
                if (atras):
                	for i in range(x_y[0], anterior[0]+1):
                    	letter_location = (i * BOX_SIZE + 18, y * BOX_SIZE + 17)
                        g.DrawText('{}'.format(matriz[x_y[0]][i]), letter_location, color=color, font=fuente+' '+str(BOX_SIZE))
                else:
                	for i in range(anterior[0], x_y[0]+1):
                    	letter_location = (i * BOX_SIZE + 18, y * BOX_SIZE + 17)
                        g.DrawText('{}'.format(matriz[x_y[0]][i]), letter_location, color=color, font=fuente+' '+str(BOX_SIZE))
                if palabra in dic.keys():
                	if dic[palabra][0]!=tipo
						sg.Popup('¡Muy Bien! Encontraste una palabra, \n pero no es un: '+tipo)
					else:
						del dic[values[palabra][0]]
						sg.Popup('¡Felicitaciones! Haz encontrado una palabra, \n solo faltan: '+ str(len(dic.keys())))
				else:
					sg.Popup('Ups, esa no es una palabra válida')
				anterior = x_y
		victoria = (cantidades[0] < 1 and cantidades[1] < 1 and cantidades[2] < 1)
        if(victoria):
            sg.Popup('Ganaste!')
            break
	sopa_window.Close()
        
			
'''
    boxX_ant = None
    boxY_ant = None
    Borrar=True
    while True:
        event, values = sopa_window.Read()
        print(event, values)
        if event == '_GRAPH_':
            mouse = values['_GRAPH_']
            if mouse == (None, None):
                continue
            box_x = mouse[0]//BOX_SIZE
            box_y = mouse[1]//BOX_SIZE
            palabra=''
            letter_location = (box_x * BOX_SIZE + 18, box_y * BOX_SIZE + 17)
            if vertical:
                x = box_y
                y = box_x
            else:
                x = box_x
                y = box_y
            if boxX_ant == None and boxY_ant == None:
                print('entre primer if')
                g.DrawText('{}'.format(matriz[box_y][box_x]), letter_location,color="grey", font=fuente+' '+str(BOX_SIZE))
                if vertical:
                    boxX_ant = y
                    boxY_ant = x
                else:
                    boxY_ant = y
                    boxX_ant = x
            if y == boxY_ant and x != boxX_ant:
                try:
                    print('entre segundo if')
                    if( x > boxX_ant):
                        for i in range(boxX_ant, x+1):
                            letra = matriz[y][i]
                            palabra += letra.lower()
                            print(palabra)
                        atras = False
                    else:
                        for i in reversed(range(x, boxX_ant+1)):
                            letra = matriz[y][i]
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
                        for i in range(x, boxX_ant+1):
                            letter_location = (i * BOX_SIZE + 18, y * BOX_SIZE + 17)
                            g.DrawText('{}'.format(matriz[box_y][i]), letter_location,color=color, font=fuente+' '+str(BOX_SIZE))
                    else:
                        for i in range(boxX_ant, x+1):
                            letter_location = (i * BOX_SIZE + 18, y * BOX_SIZE + 17)
                            g.DrawText('{}'.format(matriz[box_y][i]), letter_location,color=color, font=fuente+' '+str(BOX_SIZE))
                    if vertical:
                        boxX_ant = y
                        boxY_ant = x
                    else:
                        boxY_ant = y
                        boxX_ant = x
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
                if vertical:
                    boxX_ant = y
                    boxY_ant = x
                else:
                    boxY_ant = y
                    boxX_ant = x
                Borrar=True
        elif event is None:
            break
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
'''

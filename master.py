import sys
import PySimpleGUI as sg
import random
from pattern.web import Wiktionary as wik
from pattern.es import parse, spelling, lexicon
import string
from datetime import datetime

"""
MIEMBROS DEL GRUPO:
CRIS, SEBASTIAN AGUSTIN
PUGLIESE, ALEJO EZEQUIEL
PISONI, FELIPE
"""




BOX_SIZE = 25 #constante que representa el tamaño de un "casillero"
COLORES = ['ROJO','VERDE','AZUL','AMARILLO','ROSA','VIOLETA']
CANTIDAD = list(range(0,11))
FUENTES = [ 'Arial' ,'Courier', 'Comic', 'Fixedsys','Times','Verdana','Helvetica' ]


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
        sg.Popup('Faltan '+str(c_sus-con['sustantivo'])+' sustantivos')
        return False
    elif not adj:
        sg.Popup('Faltan '+str(c_adj-con['adjetivo'])+' adjetivos')
        return False
    elif not ver:
        sg.Popup('Faltan '+str(c_ver-con['verbo'])+' verbos')
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


#ventana de la sopa de letras:
sopa_layout = [
                [sg.Graph((800,800), (0,450), (450,0), key='_GRAPH_', change_submits=True, drag_submits=False)]
              ]
sopa_window = sg.Window('SOPA DE LETRAS', ).Layout(sopa_layout).Finalize()
sopa_window.Disappear()



config_layout = [
                   [sg.Text('PALABRAS'),sg.Input(size=(35,1),key='PALABRA'),sg.Button('Agregar',bind_return_key=True)],
                   [sg.Listbox(values=[],size=(55,6),key='LISTA',select_mode="LISTBOX_SELECT_MODE_single", bind_return_key=True)],
                   [sg.Button('Eliminar')],
                   [sg.Text('\n')],
                   [sg.Text('                   SUSTANTIVOS   '),sg.Text('ADJETIVOS    '),sg.Text('VERBOS')],
                   [sg.Text('CANTIDAD'),sg.InputCombo(values=CANTIDAD,default_value=CANTIDAD[1],size=(10,1),key='SUSTANTIVOS'),sg.InputCombo(values=CANTIDAD,default_value=CANTIDAD[1],size=(10,1),key='ADJETIVOS'),sg.InputCombo(values=CANTIDAD,default_value=CANTIDAD[1],size=(10,1),key='VERBOS')],
                   [sg.Text(' '*5+'COLOR'),sg.InputCombo(values=COLORES,default_value=COLORES[0],size=(10,1)),sg.InputCombo(values=COLORES,default_value=COLORES[1],size=(10,1)),sg.InputCombo(values=COLORES,default_value=COLORES[2],size=(10,1))],                 
                   [sg.Text('\n')],
                   [sg.Text(' '*17+'ORIENTACION'),sg.InputCombo(values=['HORIZONTAL','VERTICAL'],size=(15,1),key='ORIENTACION')],
                   [sg.Text(' '*26+'FUENTE'),sg.InputCombo(values=FUENTES,size=(15,1),key='FUENTE')],
                   [sg.Text(' '*26+'OFICINA'),sg.InputCombo(values=[None],size=(15,1))], #values=list(oficinas.keys())                
                   [sg.Text('\n')],
                   [sg.Checkbox('SOLO MINUSCULAS',key='MINUSCULAS')],                 
                   [sg.Checkbox('AYUDA',key='AYUDA')],
                   [sg.Button('LISTO',pad=(179,1))],
                ]





    

def generar_sopa(palabras, orientacion='HORIZONTAL',fuente='Comic',minusculas=False):

    g = sopa_window.FindElement('_GRAPH_')
    
    filas=16
    columnas=16
    
    if minusculas:
        mayus_minus=string.ascii_lowercase
    else:
        mayus_minus=string.ascii_uppercase
    for row in range(filas):
        for col in range(columnas):
                g.DrawRectangle((col * BOX_SIZE + 5, row * BOX_SIZE + 3), (col * BOX_SIZE + BOX_SIZE + 5, row * BOX_SIZE + BOX_SIZE + 3), line_color='black') #se dibuja cuadrado
                box_x = (col * BOX_SIZE + 5) // BOX_SIZE
                box_y = (row * BOX_SIZE + 3) // BOX_SIZE
                letter_location = (box_x * BOX_SIZE + 18, box_y * BOX_SIZE + 17)
                g.DrawText('{}'.format(random.choice(mayus_minus)), letter_location, font=fuente+' '+'25') #se dibuja letra adentro del cuadrado



def main(argv):

    
    engine=wik(language='es')

    config_window = sg.Window('CONFIGURACION', background_color=None).Layout(config_layout)
    dic = {}
    palabras = [ ]

    contador = {'sustantivo':0,'adjetivo':0,'verbo':0 }
    
    while True:
        event, values = config_window.Read()
        if event is None:
            sys.exit()
        elif event == 'Agregar':

            

            ok = False #indica si la palabra se va a agregar a la lista o no
            palabra = values['PALABRA'].lower()
            articulo = engine.article(palabra)

            if palabra not in config_window.FindElement('LISTA').GetListValues():
                
            
                if articulo != None: #si no es None esta en wiktionary
                    print('Esta en wiktionary')

                    try:
                        seccion = articulo.sections[3].content
                        tipo = parsear_tipo(seccion)
                        descripcion = parsear_descripcion(seccion)
                    except:
                        if onPattern(palabra):
                            tipo = clasificar(palabra)
                        else:
                            tipo = sg.PopupGetText('Tipo','Ingrese el tipo de la palabra (sustantivo,adjetivo,verbo)').lower()
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
                    print(tipo,' entro por patter')
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




                        
            



        elif event == 'LISTA':
            sg.Popup('Definicion',dic[values['LISTA'][0]]['descripcion'])
            
        elif event == 'Eliminar':
            print(values)
            print(contador)
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
                minusculas = values['MINUSCULAS']
                fuente = values['FUENTE']
                orientacion = values['ORIENTACION']
            
                generar_sopa(dic,orientacion,fuente,minusculas)
                break

        
    config_window.Close()
    
    sopa_window.Reappear()
    

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
            letter_location = (box_x * BOX_SIZE + 18, box_y * BOX_SIZE + 17)
            print(box_x, box_y)



    sopa_window.Close()


if __name__ == "__main__":
    main(sys.argv[1:])


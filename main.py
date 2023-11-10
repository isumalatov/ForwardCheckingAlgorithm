import pygame
import tkinter
from tkinter import *
from tkinter.simpledialog import *
from tkinter import messagebox as MessageBox
from tablero import *
from dominio import *
from pygame.locals import *
from variable import *
import time

GREY = (190, 190, 190)
NEGRO = (100, 100, 100)
BLANCO = (255, 255, 255)

MARGEN = 5  # ancho del borde entre celdas
MARGEN_INFERIOR = 60  # altura del margen inferior entre la cuadrícula y la ventana
TAM = 60  # tamaño de la celda
FILS = 10  # número de filas del crucigrama
COLS = 10  # número de columnas del crucigrama

LLENA = "*"
VACIA = "-"


#########################################################################
# Detecta si se pulsa el botón de FC
#########################################################################
def pulsaBotonFC(pos, anchoVentana, altoVentana):
    if (
        pos[0] >= anchoVentana // 4 - 25
        and pos[0] <= anchoVentana // 4 + 25
        and pos[1] >= altoVentana - 45
        and pos[1] <= altoVentana - 19
    ):
        return True
    else:
        return False


#########################################################################
# Detecta si se pulsa el botón de AC3
#########################################################################
def pulsaBotonAC3(pos, anchoVentana, altoVentana):
    if (
        pos[0] >= 3 * (anchoVentana // 4) - 25
        and pos[0] <= 3 * (anchoVentana // 4) + 25
        and pos[1] >= altoVentana - 45
        and pos[1] <= altoVentana - 19
    ):
        return True
    else:
        return False


#########################################################################
# Detecta si se pulsa el botón de reset
#########################################################################
def pulsaBotonReset(pos, anchoVentana, altoVentana):
    if (
        pos[0] >= (anchoVentana // 2) - 25
        and pos[0] <= (anchoVentana // 2) + 25
        and pos[1] >= altoVentana - 45
        and pos[1] <= altoVentana - 19
    ):
        return True
    else:
        return False


#########################################################################
# Detecta si el ratón se pulsa en la cuadrícula
#########################################################################
def inTablero(pos):
    if (
        pos[0] >= MARGEN
        and pos[0] <= (TAM + MARGEN) * COLS + MARGEN
        and pos[1] >= MARGEN
        and pos[1] <= (TAM + MARGEN) * FILS + MARGEN
    ):
        return True
    else:
        return False


#########################################################################
# Busca posición de palabras de longitud tam en el almacen
#########################################################################
def busca(almacen, tam):
    enc = False
    pos = -1
    i = 0
    while i < len(almacen) and enc == False:
        if almacen[i].tam == tam:
            pos = i
            enc = True
        i = i + 1
    return pos


#########################################################################
# Crea un almacen de palabras
#########################################################################
def creaAlmacen():
    f = open("d0.txt", "r", encoding="utf-8")
    lista = f.read()
    f.close()
    listaPal = lista.split()
    almacen = []

    for pal in listaPal:
        pos = busca(almacen, len(pal))
        if pos == -1:  # no existen palabras de esa longitud
            dom = Dominio(len(pal))
            dom.addPal(pal.upper())
            almacen.append(dom)
        elif (
            pal.upper() not in almacen[pos].lista
        ):  # añade la palabra si no está duplicada
            almacen[pos].addPal(pal.upper())

    return almacen


#########################################################################
# Imprime el contenido del almacen
#########################################################################
def imprimeAlmacen(almacen):
    for dom in almacen:
        print(dom.tam)
        lista = dom.getLista()
        for pal in lista:
            print(pal, end=" ")
        print()


#########################################################################
# getDominio
#########################################################################
def getDominio(almacen, tamaño):
    return next((variable.lista for variable in almacen if variable.tam == tamaño), [])

#########################################################################
# Modificar Dominio
#########################################################################
def modificar_dominio(tablero, variable, posicion_Inicial, i):

    palabras_borradas = []
    
    if variable.tipo == "horizontal":

        if tablero.getCelda(posicion_Inicial[0], posicion_Inicial[1] + i).isalpha():
            
            palabras_borradas = [
                palabra
                for palabra in variable.dominio
                if any(letra != tablero.getCelda(posicion_Inicial[0], posicion_Inicial[1] + i) for i, letra in enumerate(palabra))
            ]

        for palabra_a_borrar in palabras_borradas:

            variable.dominio.remove(palabra_a_borrar)

  
    else:

        if tablero.getCelda(posicion_Inicial[0] + i, posicion_Inicial[1]).isalpha():
            
            palabras_borradas = [
                palabra
                for palabra in variable.dominio
                if any(letra != tablero.getCelda(posicion_Inicial[0] + i, posicion_Inicial[1]) for i, letra in enumerate(palabra))
            ]

        for palabra_a_borrar in palabras_borradas:

            variable.dominio.remove(palabra_a_borrar)


#########################################################################
# funcionVarH
#########################################################################
def funcionVar(tablero, direccion):

    variables = []
    dominio = []
    tam = 0
    variable_horizontal = 0
    variable_vertical = 0

    posicion_Inicial = [0, 0]

    if direccion == "H":

        for fila in range(tablero.alto):

            for columna in range(tablero.ancho):

                if tablero.getCelda(fila, columna) == '-' or tablero.getCelda(fila, columna).isalpha():

                    tam += 1

                    if columna == COLS - 1:

                        if tam > 1:

                            almacen = creaAlmacen()

                            dominio = getDominio(almacen, tam)

                            nombre = "H" + str(variable_horizontal)

                            variable = Variable(nombre, tam, dominio, "horizontal")

                            for i in range(tam):
                                variable.celdas.append([posicion_Inicial[0], posicion_Inicial[1] + i])
                                modificar_dominio(tablero, variable, posicion_Inicial, i)

                            variables.append(variable)

                            variable_horizontal += 1


                        tam = 0

                        posicion_Inicial = [fila + 1, 0]


                elif tablero.getCelda(fila, columna) == '*':

                    if tam > 0:

                        if tam > 1:

                            almacen = creaAlmacen()

                            dominio = getDominio(almacen, tam)

                            nombre = "H" + str(variable_horizontal)

                            variable = Variable(nombre, tam, dominio, "horizontal")

                            for i in range(tam):
                                variable.celdas.append([posicion_Inicial[0], posicion_Inicial[1] + i])
                                modificar_dominio(tablero, variable, posicion_Inicial, i)
                            
                            variables.append(variable)

                            variable_horizontal += 1


                        tam = 0


                    if columna == COLS - 1:
                        posicion_Inicial = [fila + 1, 0]
                    else:
                        posicion_Inicial = [fila, columna + 1]
            
    else:

        for columna in range(tablero.ancho):

            for fila in range(tablero.alto):

                if tablero.getCelda(fila, columna) == '-' or tablero.getCelda(fila, columna).isalpha():

                    tam += 1

                    if fila == FILS - 1:

                        if tam > 1:

                            almacen = creaAlmacen()

                            dominio = getDominio(almacen, tam)

                            nombre = "V" + str(variable_vertical)

                            variable = Variable(nombre, tam, dominio, "vertical")

                            for i in range(tam):
                                variable.celdas.append([posicion_Inicial[0] + i, posicion_Inicial[1]])
                                modificar_dominio(tablero, variable, posicion_Inicial, i)
                                
                            variables.append(variable)

                            variable_vertical += 1

                        tam = 0

                        posicion_Inicial = [0, columna + 1]


                elif tablero.getCelda(fila, columna) == '*':

                    if tam > 0:

                        if tam > 1:

                            almacen = creaAlmacen()

                            dominio = getDominio(almacen, tam)

                            nombre = "V" + str(variable_vertical)

                            variable = Variable(nombre, tam, dominio, "vertical")

                            for i in range(tam):
                                variable.celdas.append([posicion_Inicial[0] + i, posicion_Inicial[1]])
                                modificar_dominio(tablero, variable, posicion_Inicial, i)
                                
                            variables.append(variable)

                            variable_vertical += 1

                        tam = 0


                    if fila == FILS - 1:
                        posicion_Inicial = [0, columna + 1]
                    else:
                        posicion_Inicial = [fila + 1, columna]

    return variables


#########################################################################
# Crear restricciones en las variables
#########################################################################
def funcionRestriccion(varH, varV):
    
    for h in varH:
        for v in (varV):
            encontrado = False     
            for hres in h.celdas:
                if encontrado:
                    break
                for vres in v.celdas:
                    if hres == vres:
                        h.restricciones.append(v)
                        v.restricciones.append(h)
                        encontrado = True
                        break


######################################################################### 
# Algoritmo Forward Checking
#########################################################################

def getCelda_Restringida(variable, variable_restringida):

    for casilla in variable.celdas:

        if casilla in variable_restringida.celdas:

            celda_restriccion = casilla
            break

    return celda_restriccion

def comprobar_restricciones(variable):

    variable_palabra_valido = True

    for posicion, variable_restringida in enumerate(variable.restricciones):

        celda_restriccion = getCelda_Restringida(variable, variable_restringida)
        palabras_borradas = []

        for palabra in variable_restringida.dominio:

            index_variable = variable.celdas.index(celda_restriccion)
            index_variable_restringida = variable_restringida.celdas.index(celda_restriccion)
        
            if variable.valor[index_variable] != palabra[index_variable_restringida]:

                palabras_borradas.append(palabra)
                variable_restringida.se_ha_borrado = True

        if variable_restringida.se_ha_borrado:

            for palabra_borrada in palabras_borradas:
                variable_restringida.dominio.remove(palabra_borrada)

            variable_restringida.palabras_borradas[variable.nombre] = palabras_borradas  

        if len(variable_restringida.dominio) == 0:

            variable_palabra_valido = False

            for i in range(posicion + 1):

                if variable.restricciones[i].se_ha_borrado:

                    variable.restricciones[i].se_ha_borrado = False

                    if variable.nombre in variable.restricciones[i].palabras_borradas:
                        
                        for palabra_borrada in variable.restricciones[i].palabras_borradas[variable.nombre]:
                            
                            variable.restricciones[i].dominio.append(palabra_borrada)

                        del variable.restricciones[i].palabras_borradas[variable.nombre]
    

            break

    return variable_palabra_valido


def recuperar_valores_variableHorizontal(variablesHorizontales, variable, i):

    almacen = creaAlmacen()

    variable.dominio = getDominio(almacen, variable.tam)
    i -= 1
    variablesHorizontales[i].dominio.pop(0)

    for variable_restringida in variablesHorizontales[i].restricciones:

        if variablesHorizontales[i].nombre in variable_restringida.palabras_borradas:
            
            for palabra_borrada in variable_restringida.palabras_borradas[variablesHorizontales[i].nombre]:
                
                variable_restringida.dominio.append(palabra_borrada)

            del variable_restringida.palabras_borradas[variablesHorizontales[i].nombre]
        

def fc(variablesHorizontales):

    res = True
    i = 0

    while i < len(variablesHorizontales):
        
        variable = variablesHorizontales[i]

        while variable.dominio:
  
            variable.valor = variable.dominio[0]
            variable_palabra_valido = True

            variable_palabra_valido = comprobar_restricciones(variable)

            if variable_palabra_valido == False:
                variable.dominio.pop(0)
            else:
                break
                

        if variable.dominio:

            i += 1

        else:

            if i > 0:

                recuperar_valores_variableHorizontal(variablesHorizontales, variable, i)
                
            else:

                res =  False
                break

    return res


def ForwardChecking(tablero, variables, pulsado_ac3):

    varH = []
    varV = []

    if pulsado_ac3 == False:

        varH = funcionVar(tablero, "H")
        varV = funcionVar(tablero, "V")

        funcionRestriccion(varH, varV)

    else:

        varH = variables[0]
        varV = variables[1]   

    resultado = fc(varH)

    if resultado:
        for variable in varV:
            variable.valor = variable.dominio[0]

    vT = varH + varV

    if resultado:

        for v in range(len(vT)):

            for l in range(len(vT[v].valor)):

                tablero.setCelda(vT[v].celdas[l][0], 
                                vT[v].celdas[l][1], 
                                vT[v].valor[l])
                
        
    return resultado


######################################################################### 
# Algoritmo AC3
#########################################################################
def AC3(tablero):
    
    varH = []
    varV = []

    varH = funcionVar(tablero, "H")
    varV = funcionVar(tablero, "V")

    funcionRestriccion(varH, varV) 

    print("DOMINIOS ANTES DEL AC3")

    for i in varH:
       print(i)

    for j in varV:
       print(j)

    
    restriccion_lista = []

    restriccion_lista = [[v, r] for var_list in [varH, varV] for v in var_list for r in v.restricciones]

    no_hay_solucion = False

    while restriccion_lista:

        if no_hay_solucion:
            break

        pareja_nueva = restriccion_lista[0]

        palabras_borradas_nuevas = []

        borrado_nuevo = False

        for palabra1_nueva in pareja_nueva[0].dominio:

            if no_hay_solucion:
                break

            palabra_valida_nueva = False

            for palabra2_nueva in pareja_nueva[1].dominio:

                celda_restriccion_nueva = None

                for casilla_nueva in pareja_nueva[0].celdas:

                    if casilla_nueva in pareja_nueva[1].celdas:

                        celda_restriccion_nueva = casilla_nueva
                        break

                index_primera_variable = pareja_nueva[0].celdas.index(celda_restriccion_nueva)
                index_segunda_variable = pareja_nueva[1].celdas.index(celda_restriccion_nueva)

                if (palabra1_nueva[index_primera_variable] == 
                    palabra2_nueva[index_segunda_variable]):
                    
                    palabra_valida_nueva = True

            if not palabra_valida_nueva:
                borrado_nuevo = True
                palabras_borradas_nuevas.append(palabra1_nueva)

        if borrado_nuevo:

            for restriccion_nueva in pareja_nueva[0].restricciones:
                        
                if [restriccion_nueva, pareja_nueva[0]] not in restriccion_lista:
                    restriccion_lista.append([restriccion_nueva, pareja_nueva[0]])

        for palabra_nueva in palabras_borradas_nuevas:

            pareja_nueva[0].dominio.remove(palabra_nueva)

        if len(pareja_nueva[0].dominio) == 0:

            no_hay_solucion = True
            break

        restriccion_lista.pop(0)


    print("DOMINIOS DESPUES DEL AC3")

    for i in varH:
       print(i)

    for j in varV:
       print(j)

    if no_hay_solucion:
        MessageBox.showwarning("Alerta", "No hay solución")

    return [varH, varV]


#########################################################################  
# Principal
#########################################################################
def main():
    root= tkinter.Tk() #para eliminar la ventana de Tkinter
    root.withdraw() #se cierra
    pygame.init()
    
    reloj=pygame.time.Clock()
    
    anchoVentana=COLS*(TAM+MARGEN)+MARGEN
    altoVentana= MARGEN_INFERIOR+FILS*(TAM+MARGEN)+MARGEN
    
    dimension=[anchoVentana,altoVentana]
    screen=pygame.display.set_mode(dimension) 
    pygame.display.set_caption("Practica 1: Crucigrama")
    
    botonFC=pygame.image.load("botonFC.png").convert()
    botonFC=pygame.transform.scale(botonFC,[50, 30])
    
    botonAC3=pygame.image.load("botonAC3.png").convert()
    botonAC3=pygame.transform.scale(botonAC3,[50, 30])
    
    botonReset=pygame.image.load("botonReset.png").convert()
    botonReset=pygame.transform.scale(botonReset,[50,30])
    
    pulsado_ac3 = False
    variables = [[], []]
    game_over=False
    tablero=Tablero(FILS, COLS)    
    while not game_over:
        for event in pygame.event.get():
            if event.type==pygame.QUIT:               
                game_over=True
            if event.type==pygame.MOUSEBUTTONUP:                
                #obtener posición y calcular coordenadas matriciales                               
                pos=pygame.mouse.get_pos()                
                if pulsaBotonFC(pos, anchoVentana, altoVentana):
                    print("FC")
                    #aquí llamar al forward checking
                    start_time = time.perf_counter()
                    res = ForwardChecking(tablero, variables, pulsado_ac3)
                    end_time = time.perf_counter()
                    print("Tiempo de ejecución FC: ", end_time - start_time)
                    if res==False:
                        MessageBox.showwarning("Alerta", "No hay solución")                                  
                elif pulsaBotonAC3(pos, anchoVentana, altoVentana):                    
                    print("AC3")
                    pulsado_ac3 = True
                    start_time_ac3 = time.perf_counter()
                    variables = AC3(tablero)
                    end_time_ac3 = time.perf_counter()
                    print("Tiempo de ejecución AC3: ", end_time_ac3 - start_time_ac3)
                elif pulsaBotonReset(pos, anchoVentana, altoVentana):       
                    pulsado_ac3 = False            
                    tablero.reset()
                elif inTablero(pos):
                    colDestino=pos[0]//(TAM+MARGEN)
                    filDestino=pos[1]//(TAM+MARGEN)                    
                    if event.button==1: #botón izquierdo
                        if tablero.getCelda(filDestino, colDestino)==VACIA:
                            tablero.setCelda(filDestino, colDestino, LLENA)
                        else:
                            tablero.setCelda(filDestino, colDestino, VACIA)
                    elif event.button==3: #botón derecho
                        c=askstring('Entrada', 'Introduce carácter')
                        tablero.setCelda(filDestino, colDestino, c.upper())

        ##código de dibujo
        # limpiar pantalla
        screen.fill(NEGRO)
        pygame.draw.rect(
            screen, GREY, [0, 0, COLS * (TAM + MARGEN) + MARGEN, altoVentana], 0
        )
        for fil in range(tablero.getAlto()):
            for col in range(tablero.getAncho()):
                if tablero.getCelda(fil, col) == VACIA:
                    pygame.draw.rect(
                        screen,
                        BLANCO,
                        [
                            (TAM + MARGEN) * col + MARGEN,
                            (TAM + MARGEN) * fil + MARGEN,
                            TAM,
                            TAM,
                        ],
                        0,
                    )
                elif tablero.getCelda(fil, col) == LLENA:
                    pygame.draw.rect(
                        screen,
                        NEGRO,
                        [
                            (TAM + MARGEN) * col + MARGEN,
                            (TAM + MARGEN) * fil + MARGEN,
                            TAM,
                            TAM,
                        ],
                        0,
                    )
                else:  # dibujar letra
                    pygame.draw.rect(
                        screen,
                        BLANCO,
                        [
                            (TAM + MARGEN) * col + MARGEN,
                            (TAM + MARGEN) * fil + MARGEN,
                            TAM,
                            TAM,
                        ],
                        0,
                    )
                    fuente = pygame.font.Font(None, 70)
                    texto = fuente.render(tablero.getCelda(fil, col), True, NEGRO)
                    screen.blit(
                        texto,
                        [
                            (TAM + MARGEN) * col + MARGEN + 15,
                            (TAM + MARGEN) * fil + MARGEN + 5,
                        ],
                    )
        # pintar botones
        screen.blit(botonFC, [anchoVentana // 4 - 25, altoVentana - 45])
        screen.blit(botonAC3, [3 * (anchoVentana // 4) - 25, altoVentana - 45])
        screen.blit(botonReset, [anchoVentana // 2 - 25, altoVentana - 45])
        # actualizar pantalla
        pygame.display.flip()
        reloj.tick(40)
        if game_over == True:  # retardo cuando se cierra la ventana
            pygame.time.delay(500)

    pygame.quit()


if __name__ == "__main__":
    main()

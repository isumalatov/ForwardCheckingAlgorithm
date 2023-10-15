import pygame
import tkinter
from tkinter import *
from tkinter.simpledialog import *
from tkinter import messagebox as MessageBox
from tablero import *
from dominio import *
from pygame.locals import *
from variable import *

GREY = (190, 190, 190)
NEGRO = (100, 100, 100)
BLANCO = (255, 255, 255)

MARGEN = 5  # ancho del borde entre celdas
MARGEN_INFERIOR = 60  # altura del margen inferior entre la cuadrícula y la ventana
TAM = 60  # tamaño de la celda
FILS = 5  # número de filas del crucigrama
COLS = 6  # número de columnas del crucigrama

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
    dominio = []

    for i in range(len(almacen)):
        if almacen[i].tam == tamaño:
            dominio = almacen[i].lista
            break

    return dominio


#########################################################################
# funcionVarH
#########################################################################
def funcionVar(tablero, almacen, direccion):
    posI = [0, 0]

    celdasVacias = 0
    variables = []
    dominio = []

    for fila in range(tablero.alto):
        for columna in range(tablero.ancho):
            if direccion == "H" and tablero.getCelda(fila, columna) == "-":
                celdasVacias += 1

                if columna == tablero.ancho - 1:
                    dominio = getDominio(almacen, celdasVacias)
                    variable = Variable(celdasVacias, dominio)

                    for i in range(celdasVacias):
                        variable.celda.append([posI[0], posI[1] + i])

                    variables.append(variable)
                    celdasVacias = 0
                    posI = [fila + 1, 0]

            elif direccion == "V" and tablero.getCelda(fila, columna) == "-":
                celdasVacias += 1

                if fila == tablero.alto - 1:
                    dominio = getDominio(almacen, celdasVacias)
                    variable = Variable(celdasVacias, dominio)

                    for i in range(celdasVacias):
                        variable.celda.append([posI[0] + i, posI[1]])

                    variables.append(variable)
                    celdasVacias = 0
                    posI = [0, columna + 1]

            elif tablero.getCelda(fila, columna) == "*":
                if celdasVacias > 0:
                    dominio = getDominio(almacen, celdasVacias)
                    variable = Variable(celdasVacias, dominio)

                    if direccion == "H":
                        for i in range(celdasVacias):
                            variable.celda.append([posI[0], posI[1] + i])
                    elif direccion == "V":
                        for i in range(celdasVacias):
                            variable.celda.append([posI[0] + i, posI[1]])

                    variables.append(variable)
                    celdasVacias = 0

                if direccion == "H":
                    if columna == tablero.ancho - 1:
                        posI = [fila + 1, 0]
                    else:
                        posI = [fila, columna + 1]
                elif direccion == "V":
                    if fila == tablero.alto - 1:
                        posI = [0, columna + 1]
                    else:
                        posI = [fila + 1, columna]

    return variables


#########################################################################
# Crear restricciones en las variables
#########################################################################
def funcionRestriccion(varH, varV):
    for i in range(len(varH)):
        celdas_comparadas = set()
        for casillaH in varH[i].celda:
            for j in range(len(varV)):
                if j not in varH[i].restriccionC:  # Evitar comparaciones repetidas
                    for casillaV in varV[j].celda:
                        if casillaH == casillaV:
                            varH[i].restriccionC.append(varV[j])
                            varV[j].restriccionC.append(varH[i])
                            celdas_comparadas.add(casillaH)


#########################################################################
# Algoritmo Forward Checking
#########################################################################
def ForwardChecking(tablero, almacen):
    varH = []
    varV = []
    varH = funcionVar(tablero, almacen, "H")
    varV = funcionVar(tablero, almacen, "V")

    funcionRestriccion(varH, varV)

    return False


#########################################################################
# Principal
#########################################################################
def main():
    root = tkinter.Tk()  # para eliminar la ventana de Tkinter
    root.withdraw()  # se cierra
    pygame.init()

    reloj = pygame.time.Clock()

    anchoVentana = COLS * (TAM + MARGEN) + MARGEN
    altoVentana = MARGEN_INFERIOR + FILS * (TAM + MARGEN) + MARGEN

    dimension = [anchoVentana, altoVentana]
    screen = pygame.display.set_mode(dimension)
    pygame.display.set_caption("Practica 1: Crucigrama")

    botonFC = pygame.image.load("botonFC.png").convert()
    botonFC = pygame.transform.scale(botonFC, [50, 30])

    botonAC3 = pygame.image.load("botonAC3.png").convert()
    botonAC3 = pygame.transform.scale(botonAC3, [50, 30])

    botonReset = pygame.image.load("botonReset.png").convert()
    botonReset = pygame.transform.scale(botonReset, [50, 30])

    almacen = creaAlmacen()
    game_over = False
    tablero = Tablero(FILS, COLS)
    while not game_over:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                game_over = True
            if event.type == pygame.MOUSEBUTTONUP:
                # obtener posición y calcular coordenadas matriciales
                pos = pygame.mouse.get_pos()
                if pulsaBotonFC(pos, anchoVentana, altoVentana):
                    print("FC")
                    # aquí llamar al forward checking
                    res = ForwardChecking(tablero, almacen)
                    if res == False:
                        MessageBox.showwarning("Alerta", "No hay solución")
                elif pulsaBotonAC3(pos, anchoVentana, altoVentana):
                    print("AC3")
                elif pulsaBotonReset(pos, anchoVentana, altoVentana):
                    tablero.reset()
                elif inTablero(pos):
                    colDestino = pos[0] // (TAM + MARGEN)
                    filDestino = pos[1] // (TAM + MARGEN)
                    if event.button == 1:  # botón izquierdo
                        if tablero.getCelda(filDestino, colDestino) == VACIA:
                            tablero.setCelda(filDestino, colDestino, LLENA)
                        else:
                            tablero.setCelda(filDestino, colDestino, VACIA)
                    elif event.button == 3:  # botón derecho
                        c = askstring("Entrada", "Introduce carácter")
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

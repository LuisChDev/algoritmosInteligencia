from os import system
from time import sleep
import os
import pdb


# generador de grid.
# cada elemento del grid es una tupla conteniendo:
# 1.- una tupla de dos enteros, representando las coordenadas,
# 2.- la (futura) distancia del punto de partida hasta allí.
def makeGrid(length,  # numero de filas
             width,   # numero de columnas
             obs):    # lista de coordenadas marcando obstáculos
    grid = []
    for i in range(0, length + 2):
        row = []
        if (i == 0 or i == length + 1):
            row = [[(i, j), -2] for j in range(0, width + 2)]
        else:
            row = []
            row.append([(i, 0), -2])
            for j in range(1, width + 1):
                if ((i, j) in obs):
                    row.append([(i, j), -2])
                else:
                    row.append([(i, j), 0])
            row.append([(i, width + 1), -2])
        grid.append(row)
    return grid


def printGrid(grid):
    for row in grid:
        print('  '.join([' ' + str(x[1]) if x[1] >= 0 else str(x[1])
                         for x in row]))
        print("\n")


# Von Neumann neighborhood
def checkBoors(coords):
    return [(coords[0] - 1, coords[1]),  # left
            (coords[0], coords[1] - 1),  # up
            (coords[0] + 1, coords[1]),  # right
            (coords[0], coords[1] + 1)]  # down


# Moore neighborhood
def mooreBoors(coords):
    return [(coords[0] - 1, coords[1]),      # left
            (coords[0] - 1, coords[1] - 1),   # upper-left corner
            (coords[0], coords[1] - 1),      # up
            (coords[0] + 1, coords[1] - 1),  # upper-right corner
            (coords[0] + 1, coords[1]),      # right
            (coords[0] + 1, coords[1] + 1),  # lower-right corner
            (coords[0], coords[1] + 1),      # down
            (coords[0] - 1, coords[1] + 1)]  # lower-left corner


# each iteration in the wavefront algorithm.
# takes the previous front of the wave, checks all the neighbours, and adds
# the zeroed ones to the newt wavefront list, before relabeling them with
# their value.
# the end point is marked with a -1. Once found, execution halts and grid is
# returned as is.
def wavefrontStep(front, grd, hoodMethod):
    nextFront = []
    for block in front:
        for neigh in [grd[x[0]][x[1]] for x in checkBoors(block[0])]:
            if neigh[1] == -1:
                # pdb.set_trace()
                neigh[1] = block[1] + 1
                # set every remaining value of the grid with a placeholder
                for row in grd:
                    for cell in grd:
                        if cell[1] == 0:
                            cell[1] = block[1] + 2
                return grd
            elif neigh[1] == 0:
                neigh[1] = block[1] + 1
                # pdb.set_trace()
                nextFront.append(neigh)
    print(''.join([str(x[0]) for x in nextFront]))
    return (nextFront, grd)


# iterate the algorithm until a path is found.
def wavefront(start, end, grd, hoodMethod):
    # set the starting position with value 1.
    grd[start[0][0]][start[0][1]] = [start[0], 1]
    # ponerle -1 a la posición final.
    grd[end[0][0]][end[0][1]] = [end[0], -1]

    grid = ([start], grd)  # wavefrontStep([start], grd, hoodMethod)
    # either the solution is found, or the wavefront vanishes, meaning
    # there is no path.
    while (len(grid) == 2 and len(grid[1]) > 0):
        os.system('clear')
        os.system('cls')
        printGrid(grid[1])
        grid = wavefrontStep(grid[0], grid[1], hoodMethod)
        sleep(1)
    # this means grd will have a single element if there is a path, or
    # two elements if no path can be found.
    return grd


# take the final grid and return the path in terms of movement instructions.
def pathToBeTaken(grid, end, hoodMethod):
    # this list contains the path traversed.
    # las diferentes posiciones son representadas de la siguiente forma:
    # ESTE - NORESTE - NORTE - NOROESTE - OESTE - SUROESTE - SUR - SURESTE
    path = []
    path.append(end)

    # mientras no hallemos el valor 1 (que indica el comienzo), continuamos
    # buscando, y añadimos el siguiente paso a la lista.
    boors = [grid[x[0]][x[1]] for x in hoodMethod(end[0])]
    nextStep = end  # next(x for x in boors if x[1] == end[1] - 1)
    while 1 not in [x[1] for x in boors]:
        # get next step
        # pdb.set_trace()
        nextStep = next(x for x in boors if x[1] == nextStep[1] - 1)
        # add it to the list
        path.append(nextStep)
        # and we call the function again
        boors = [grid[x[0]][x[1]] for x in hoodMethod(nextStep[0])]
    # calculate final step and return path
    path.append(next(x for x in boors if x[1] == 1))
    # relacionar cada cambio de coordenadas con un posible movimiento.
    movements = {
        (0, -1): "NORTE",
        (0, 1): "SUR",
        (1, 0): "ESTE",
        (-1, 0): "OESTE",
        (-1, -1): "NOROESTE",
        (1, -1): "NORESTE",
        (1, 1): "SURESTE",
        (-1, 1): "SUROESTE"
    }
    # por cada valor en la lista de posiciones, sustraer sus coordenadas de las
    # de la posición posterior. El resultado se compara con el diccionario
    # arriba y se añade la dirección al resultado.
    directions = []
    for i, x in enumerate(path[::-1]):  # reverse the list so steps are in the
                                        # right order
        # pdb.set_trace()
        longitud = x[0][0] - path[::-1][i - 1][0][0]
        latitud = x[0][1] - path[::-1][i - 1][0][1]
        directions.append(movements.get((longitud, latitud), "bad data"))

    # delete the first element of the array, as it makes no sense
    directions = directions[1:]
    return directions


# esta función calcula finalmente la lista de pasos para ir de principio a fin.
# def listaDePasos(path):



if __name__ == "__main__":
    print("bienvenido al generador de caminos.")
    fs = input("por favor ingrese el numero de filas en su mapa.")
    cs = input("Ahora ingrese el número de columnas.")
    obs = []
    obsP = input("desea ingresar obstáculos? (Y/N)")
    while obsP == "Y":
        x = input("ingrese la coordenada x: ")
        y = input("ingrese la coordenada y: ")
        coord = (int(x), int(y))
        obs.append(coord)
        obsP = input("desea ingresar otra coordenada? (Y/N)")

    print("su mapa está listo:")
    newGrid = makeGrid(int(fs), int(cs), obs)
    printGrid(newGrid)
    x = input("ingrese la coordenada x del punto de partida.")
    y = input(" Ingrese la coordenada Y del punto de partida.")
    init = (int(x), int(y))
    x = input("ingrese la coordenada x del punto de llegada.")
    y = input(" Ingrese la coordenada Y del punto de llegada.")
    end = (int(x), int(y))
    meth = input("Finalmente, indique si las casillas en diagonal se consi"
                 "deran vecinas. (Y/N)")
    if meth == 'Y':
        neighMethod = mooreBoors
    else:
        neighMethod = checkBoors

    print("Su camino está siendo calculado.")
    initBlock = newGrid[init[0]][init[1]]
    endBlock = newGrid[end[0]][end[1]]
    result = wavefront(initBlock, endBlock, newGrid, neighMethod)
    if isinstance(result, list):
        print("este es el resultado:")
        printGrid(result)
        endBlock = result[end[0]][end[1]]
        print("El camino final es este: ")
        path = pathToBeTaken(result, endBlock, neighMethod)
        print(path)
    else:
        print("No parece haber una solución :(")

from random import random
from copy import copy
from math import floor, sqrt
import pdb
# algoritmo de optimización local en python
# Luis Eduardo Chavarriaga Cifuentes - T00056784


# esta función toma una solución y retorna todos sus vecinos inmediatos en el
# espacio de búsqueda.
# para el propósito de este algoritmo, se consideran vecinas las soluciones que
# se diferencian de la original en el cambio de la posición de dos ciudades.
# esto es un total de (n^2 - n)/2 soluciones.
# lista provisional: 12.48 15.32 69.20 57.32 67.12 68.23 43.55
def vecinos(solucion):
    # pdb.set_trace()
    vecs = []
    j = 0
    while(j < len(solucion) - 1):
        i = j + 1
        while(i < len(solucion)):
            sol = copy(solucion)
            val1 = sol[i]
            val2 = sol[j]
            sol[i] = val2
            sol[j] = val1
            vecs.append(sol)
            i = i + 1
        sol = sol[1:]
        j = j + 1
    return vecs


# def vecinos2(solucion):
#     vecs = []
#     i = 0
#     while(i < len(solucion) - 1):
#         j = i + 1
#         while(j < len(solucion)):
#             print(solucion)
#             val1 = solucion[i]
#             print(solucion)
#             val2 = solucion[j]
#             print(solucion)
#             vecs.append(modifyList(j, val1, modifyList(i, val2, solucion)))
#             print(solucion)
#             print(vecs)
#             j = j + 1
#         i = i + 1
#     return vecs


# def modifyList(index, element, lista):
#     lista[index] = element
#     return lista


# esta función genera una solución aleatoria inicial al problema.
def inicial(ciudades):
    cities = ciudades
    initSol = []
    while len(cities) > 0:
        rand = floor(random()*len(cities))
        nextCity = cities[rand]
        initSol.append(nextCity)
        cities = cities[:rand] + cities[(rand + 1):]
    return initSol


# esta función calcula las distancias entre las ciudades dadas por el usuario.
def calcDistances(ciudades):
    # pdb.set_trace()
    distances = []
    for i in range(0, len(ciudades)):
        row = []
        for j in range(0, len(ciudades)):
            row.append(sqrt((ciudades[i][0] - ciudades[j][0])**2
                            + (ciudades[i][1] - ciudades[j][1])**2))
        distances.append(row)
    return distances


# esta función calcula la distancia total recorrida por el viajero en una
# solución.
# las rutas se proporcionan en el orden en que aparecen en la matriz.
def routeCost(ruta, distances):
    costo = 0
    for i in range(0, len(ruta)):
        # pdb.set_trace()
        costo = costo + distances[ruta[i - 1]][ruta[i]]
    return costo


# leer lista de ciudades y parsear
# lista provisional: 12.48 15.32 69.20 57.32 67.12 68.23 43.55
def citiesFromLista(cadena):
    coordList = cadena.split(' ')
    cityList = []
    for x in coordList:
        values = x.split('.')
        cityList.append((int(values[0]), int(values[1])))
    return cityList


# paso de optimización. Se toma la solución actual, se genera la vecindad, y
# se chequean los costos. Se retorna la solución con el menor costo. Si la
# solución con el menor costo es la original, se envía una señal que interrumpe
# el algoritmo.
def pasoOpt(solucion, distances):
    # paso 1. se genera la vecindad
    # pdb.set_trace()
    vecinosList = vecinos(solucion)
    # paso 2. se chequea el costo de cada uno de los vecinos
    cheapest = vecinosList[0]
    cheapestCost = routeCost(cheapest, distances)
    for x in vecinosList:
        costX = routeCost(x, distances)
        if costX < cheapestCost:
            cheapest = x
            cheapestCost = costX
    # pdb.set_trace()
    # paso 3. Finalmente, si alguno de los vecinos es más barato que el
    # original, se envía. Si el original sigue siendo más barato, se señala
    # el fin del algoritmo.
    if routeCost(solucion, distances) < cheapestCost:
        return (solucion, False)
    else:
        return cheapest


# main loop.
# se ejecutan pasos de optimización hasta que no es posible más.
def optimizar(init, cityList, distances):
    # pdb.set_trace()
    solucionFinal = cityList
    while not isinstance(solucionFinal, tuple):
        print("El costo de la solucion actual es: ",
              routeCost(solucionFinal, distances))
        solucionFinal = pasoOpt(solucionFinal, distances)
    return solucionFinal[0]


# pide una coordenada.
def askCoord():
    try:
        x = int(input("ingrese la coordenada X: "))
        y = int(input("ingrese la coordenada Y: "))
    except ValueError:
        return("Los valores ingresados no son números. Intenta de nuevo")
    return (x, y)


if __name__ == "__main__":
    print("Este programa optimizará la ruta de un viajero entre las ciudades"
          " especificadas por el usuario.")
    cities = []
    ans = input("desea ingresar una ciudad? (Y/N) ")
    while(ans != "N"):
        coords = askCoord()
        while not isinstance(coords, tuple):
            print(coords)
            coords = askCoord()
        cities.append(coords)
        ans = input("desea ingresar una más? (Y/N)")

    ans = input("ingrese ciudades en una lista: ")
    cities = cities + citiesFromLista(ans)
    # generando un hash con las ciudades en sus posiciones
    cityList = dict(zip(range(0, len(cities)), cities))

    print("las ciudades, en su orden, son: ")
    print(cityList)

    # se le pasan las llaves al generador de soluciones
    solInicial = inicial(list(cityList.keys()))
    print("la solución inicial es:")
    print(solInicial)

    init = input("ingrese la posición de la primera ciudad en la lista: ")
    init = int(init)

    distances = calcDistances(cities)
    # print(distances)
    print("el costo de esta primera solución es:")
    print(routeCost(solInicial, distances))

    print("se está calculando su solución óptima.")
    finalSol = optimizar(init, solInicial, distances)

    indx = finalSol.index(init)
    print("la solución final es: ", finalSol[indx:] + finalSol[:indx])
    print("El costo es: ", routeCost(finalSol, distances))

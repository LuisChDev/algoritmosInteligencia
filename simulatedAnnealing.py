from hillClimbing import (inicial, calcDistances, routeCost, askCoord,
                          citiesFromLista)
from copy import copy
from random import random, randint
from time import sleep
from math import floor
import pdb
import os


# función que calcula la probabilidad de aceptación de una solución con peor
# desempeño que la original.
def probabilidad(sol, newsol, temp):
    return (2.71)**((-1)*((newsol - sol)/(temp)))


# función que genera una nueva solución aleatoriamente, variando la original.
def newSolution(solution):
    # pdb.set_trace()
    first = floor(randint(0, len(solution) - 1))
    second = floor(randint(0, len(solution) - 1))
    newSolution = copy(solution)
    newSolution[first] = solution[second]
    newSolution[second] = solution[first]
    return newSolution


# paso de optimización.
# generar una solución aleatoria, calcular su desempeño y decidir si desplaza
# a la original.
def pasoOpt(solucion, temp, distances):
    # paso 1. generar una solución.
    newSol = newSolution(solucion)
    # paso 2. calcular su desempeño
    perfSol = routeCost(newSol, distances)
    # paso 3. si es mejor que la original...
    if (perfSol < routeCost(solucion, distances)):
        # retornar la nueva solución
        return newSol
    # si no...
    else:
        # paso 4. calcular la probabilidad de aceptación
        prob = probabilidad(routeCost(solucion, distances), perfSol, temp)
        # paso 5. generar un número aleatorio entre 0 y 1.
        number = random()
        # paso 6. si es menor que la probabilidad...
        if (number < prob):
            # retornar la nueva solucion
            return newSol
        # si no...
        else:
            # retornar la solución original
            return solucion


# loop de optimización.
# se termina de ejecutar una vez la temperatura llegue al mínimo.
def optimizar(solInicial, distances, temp):
    temperatura = temp
    sol = solInicial
    # se dan pasos de optimización hasta que la temperatura llegue a uno
    while temperatura > 1:
        sol = pasoOpt(sol, temperatura, distances)
        os.system('clear')
        os.system('cls')
        print("El costo del modelo actual es: ", routeCost(sol, distances))
        sleep(0.25)
        temperatura = temperatura - 1
    return sol


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
    finalSol = optimizar(solInicial, distances, 100)

    indx = finalSol.index(init)
    print("la solución final es: ", finalSol[indx:] + finalSol[:indx])
    print("la solución inicial era: ", solInicial)
    print("El costo inicial era: ", routeCost(solInicial, distances))
    print("El costo es: ", routeCost(finalSol, distances))

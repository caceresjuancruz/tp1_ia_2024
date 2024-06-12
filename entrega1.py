from itertools import takewhile
from simpleai.search import (SearchProblem, astar, greedy)
from simpleai.search.viewers import (BaseViewer, WebViewer)

def cerrado(frasco):
        return len(frasco) == 4 and len(set(frasco)) == 1

class LlenadoDeFrascosProblem(SearchProblem):
    def actions(self, state):
        acciones_disponibles = []
        for indice_origen, origen in enumerate(state):
            if origen and not cerrado(origen):
                for indice_destino, destino in enumerate(state):
                    if indice_origen != indice_destino and len(destino) < 4:
                        if not destino or origen[-1] == destino[-1]:
                            acciones_disponibles.append((indice_origen, indice_destino))
        return acciones_disponibles

    def result(self, state, action):
        frascos = [list(frasco) for frasco in state]
        indice_origen, indice_destino = action

        origen = frascos[indice_origen]
        destino = frascos[indice_destino]

        color = origen[-1]

        # Obtengo los colores de origen que puedo pasar al destino
        colores_en_origen = sum(1 for _ in takewhile(lambda x: x == color, reversed(origen))) #cuenta cuántos elementos consecutivos en el frasco origen (empezando desde el final) tienen el mismo color que el color especificado. la función takewhile toma los elementos del frasco mientras que tengan el mismo color, y luego contamos cuántos elementos se han tomado y se suman para obtener el total de elementos con el color deseado.

        # Paso los colores al destino
        for _ in range(min(colores_en_origen, 4 - len(destino))):
            destino.append(origen.pop())

        return tuple(tuple(frasco) for frasco in frascos)

    def cost(self, state, action, state2):
        return 1

    def is_goal(self, state):
        return all(len(frasco) == 0 or cerrado(frasco) for frasco in state)

    def heuristic(self, state):
        costo_total = 0
        for frasco in state:
            if frasco and not cerrado(frasco):
                # Conjunto para contar colores distintos
                colores_distintos = set(frasco)
                # Restar uno para evitar sobreestimación
                costo_total += len(colores_distintos) - 1
        return costo_total

def jugar(frascos, dificil):
    problem = LlenadoDeFrascosProblem(frascos)
    if dificil:
        result = greedy(problem)
    else:
        result = astar(problem)
    pasos = []
    if result is not None:
        for action, state in result.path():
            if action:
                indice_origen, indice_destino = action
                pasos.append((indice_origen + 1, indice_destino + 1))
    else:
        print("No se encontró solución.")
    return pasos


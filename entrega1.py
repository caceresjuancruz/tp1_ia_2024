from itertools import combinations
from simpleai.search import (SearchProblem, astar, greedy)
from simpleai.search.viewers import (BaseViewer, WebViewer)

#juego de llenado de frascos de colores
#estado inicial
INICIAL = (("verde", "azul", "rojo", "naranja"),  # frasco 1
           ("azul", "rosa", "naranja"),           # frasco 2
           ("rosa", "celeste", "verde", "verde"), # frasco 3
           ("rosa", "rojo", "celeste", "celeste"),# frasco 4
           ("rojo", "azul", "lila"),              # frasco 5
           ("verde", "naranja", "celeste", "rojo"),# frasco 6
           ("azul", "naranja", "rosa"),           # frasco 7
           ("lila", "lila", "lila"),              # frasco 8
           ())                                    # frasco 9

def cerrado(frasco):
        return len(frasco) == 4 and len(set(frasco)) == 1

class LlenadoDeFrascosProblem(SearchProblem):
    def actions(self, state):
        acciones_disponibles = []
        frascos_combinados = combinations(state, 2)

        for origen, destino in frascos_combinados:
            if state.index(origen) != state.index(destino) and origen and len(destino) < 4 and not cerrado(origen) and not cerrado(destino) and destino and (origen[-1] == destino[-1] or destino == ()):
                acciones_disponibles.append((state.index(origen), state.index(destino)))

        return acciones_disponibles

    def result(self, state, action):
        state = list(state)
        origen, destino = action
        if state[origen]:
            state[destino] = state[destino] + (state[origen][-1],)
            state[origen] = state[origen][:-1]
        state = tuple(state)
        print(state)
        return state

    def cost(self, state, action, state2):
        return 1

    def is_goal(self, state):
        return all(len(frasco) == 4 and len(set(frasco)) == 1 for frasco in state)

    def heuristic(self, state):
        costo_total = 0
        for frasco in state:
            if frasco != ():
                costo_total += 4 - len(frasco)
                costo_total += len(set(frasco)) - 1
            else:
                costo_total += 4

        return costo_total

def jugar(frascos, dificil):
    problem = LlenadoDeFrascosProblem(INICIAL)
    if dificil:
        result = greedy(problem)
    else:
        result = astar(problem) #viewer=BaseViewer()
    pasos = []
    if result is not None:
        for action, state in result.path():
            origen, destino = action
            pasos.append((origen + 1, destino + 1))
    else:
        print("No se encontró solución.")
    return pasos

#jugar(INICIAL, False)


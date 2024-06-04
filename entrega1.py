from simpleai.search import (SearchProblem, astar)
from simpleai.search.viewers import (BaseViewer, WebViewer)


#juego de llenado de frascos de colores
#estado inicial
INICIAL = [("verde", "azul", "rojo", "naranja"),     # frasco 1, notar el orden de los colores
        ("azul", "rosa", "naranja"),              # frasco 2, notar que es de largo 3, queda un espacio vacío
        ("rosa", "celeste", "verde", "verde"),    # frasco 3, notar cómo "verde" se repite 2 veces por los 2 cuartos iguales
        ("rosa", "rojo", "celeste", "celeste"),   # frasco 4
        ("rojo", "azul", "lila"),                 # frasco 5
        ("verde", "naranja", "celeste", "rojo"),  # frasco 6
        ("azul", "naranja", "rosa"),              # frasco 7
        ("lila", "lila", "lila"),                 # frasco 8, notar la repetición de colores para cada cuarto
        (),]                                       # frasco 9, notar que una tupla de largo 0 es un frasco vacío

class LlenadoDeFrascosProblem(SearchProblem):
    def actions(self, state):
        acciones_disponibles = []

        for i in range(len(state)):
            for j in range(len(state)):
                if i != j and state[i] != () and len(state[j]) < 4 and (state[i][-1] == state[j][-1] or state[j] == ()):
                    acciones_disponibles.append((i, j))

        return acciones_disponibles

    def result(self, state, action):
        state = list(state)
        i, j = action
        state[j] = state[j] + (state[i][-1],)
        state[i] = state[i][:-1]
        state = tuple(state)
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
        result = astar(problem)
    else:
        result = astar(problem, viewer=BaseViewer())
    pasos = []
    for action, state in result.path():
        pasos.append(action)
    return pasos

#print(jugar(INICIAL, True))


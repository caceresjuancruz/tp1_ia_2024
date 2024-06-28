from simpleai.search import SearchProblem, greedy, astar

def cerrado(frasco):
    return len(frasco) == 4 and len(set(frasco)) == 1

class LlenadoDeFrascosProblem(SearchProblem):
    def actions(self, state):
        acciones_disponibles = []
        for indice_origen, origen in enumerate(state):
            if not len(origen) == 0 and not cerrado(origen):
                for indice_destino, destino in enumerate(state):
                    if indice_origen != indice_destino and len(destino) < 4:
                        if len(destino) == 0 or origen[-1] == destino[-1]:
                            acciones_disponibles.append((indice_origen + 1, indice_destino + 1))
        return acciones_disponibles

    def result(self, state, action):
        frascos = [list(frasco) for frasco in state]
        indice_origen, indice_destino = action
        indice_origen -= 1
        indice_destino -= 1
        
        color = frascos[indice_origen][-1]
        while frascos[indice_origen] and frascos[indice_origen][-1] == color and len(frascos[indice_destino]) < 4:
            frascos[indice_destino].append(frascos[indice_origen].pop())
        return tuple(tuple(frasco) for frasco in frascos)

    def cost(self, state, action, state2):
        return 1

    def is_goal(self, state):
        return all(len(frasco) == 0 or cerrado(frasco) for frasco in state)

    def heuristic(self, state):
        costo_total = 0
        for frasco in state:
            if not len(frasco) == 0 and not cerrado(frasco):
                colores_distintos = set(frasco)
                costo_total += len(colores_distintos) - 1
        return costo_total

def jugar(frascos, dificil):
    problem = LlenadoDeFrascosProblem(frascos)
    if dificil:
        result = greedy(problem, graph_search=True)
    else:
        result = astar(problem, graph_search=True)
    pasos = []
    for action, state in result.path():
        if action:
            pasos.append(action)
    return pasos

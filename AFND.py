class Estado:
    def __init__(self, esFinal):
        self.final = esFinal
        self.transiciones = {}

    def addTransicion(self, simbolo, destino):
        #Checa si el simbolo ya esta en el diccionario antes de hacele append
        if simbolo in self.transiciones:
            self.transiciones[simbolo].append(destino)
        else:
            self.transiciones[simbolo] = [destino]


class Graph:
    cNode = 1

    def __init__(self):
        self.estados = {}
        self.estados[0] = Estado(False)
        self.inicial = 0
        self.final = 0

    def basico(self, simbolo):
        self.estados[Graph.cNode] = Estado(True)
        self.final = Graph.cNode
        self.estados[self.inicial].addTransicion(simbolo, Graph.cNode)
        Graph.cNode += 1


    def opcional(self):# λ
        # Se crean los nuevos estados iniciales y finales
        nInicial = Graph.cNode
        nFinal = Graph.cNode+1
        Graph.cNode+=2
        self.estados[nInicial] = Estado(False)
        self.estados[nFinal] = Estado(True)
        # El nuevo inicial apunta al inicial original y al nuevo final
        self.estados[nInicial].addTransicion('λ', self.inicial)
        self.estados[nInicial].addTransicion('λ', nFinal)
        self.estados[self.final].addTransicion('λ', nFinal)
        self.estados[self.final].final=False
        # Se actualizan los estados iniciales y finales
        self.inicial = nInicial
        self.final = nFinal


test = Graph()
test.basico('a')
test.opcional()
for key, value in test.estados.items():
    print(key, value.transiciones, value.final)

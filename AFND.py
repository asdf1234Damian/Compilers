import networkx as nx
import matplotlib.pyplot as plt
from graphviz import Digraph

class Estado:
    def __init__(self,esFinal):
        # self.id = id
        self.final = esFinal
        self.transiciones = {}

    def addTransicion(self, simbolo, destino):
        #Checa si el simbolo ya esta en el diccionario antes de hacele append
        if simbolo in self.transiciones:
            self.transiciones[simbolo].append(destino)
        else:
            self.transiciones[simbolo] = [destino]


class Graph:
    cNode = 0

    def __init__(self):
        self.G = Digraph()
        self.estados = {}
        self.inicial=None
        self.final=None

    def basico(self, simbolo):
        #Se agregan el estado inicial
        self.inicial = Graph.cNode
        self.final = Graph.cNode+1
        #Se crean los estados
        self.estados[self.inicial] = Estado(False)
        self.estados[self.final] = Estado(True)
        #Se crea la transicion entre inical y final
        self.estados[self.inicial].addTransicion(simbolo,self.final)
        # Se actualiza el counter de los nodos
        Graph.cNode += 2

    def plot(self):
        for origin,states in self.estados.items():
            for simbol,destiny in states.transiciones.items():
                for end in destiny:
                    self.G.edge(str(origin), str(end), label=simbol)
                    self.G.view(filename=None, directory=None, cleanup=False)
                    print('Origin: ',origin,'simb: ',simbol, end)


    def opcional(self):# ε
        # Se crean los nuevos estados iniciales y finales
        nInicial = Graph.cNode
        nFinal = Graph.cNode+1
        Graph.cNode+=2
        self.estados[nInicial] = Estado(False)
        self.estados[nFinal] = Estado(True)
        # El nuevo inicial apunta al inicial original y al nuevo final
        self.estados[nInicial].addTransicion('ε', self.inicial)
        self.estados[nInicial].addTransicion('ε', nFinal)
        self.estados[self.final].addTransicion('ε', nFinal)
        self.estados[self.final].final=False
        # Se actualizan los estados iniciales y finales
        self.inicial = nInicial
        self.final = nFinal


test = Graph()
test.basico('a')
test.opcional()

test1 = Graph()
test1.basico('a')
test1.opcional()
test1.opcional()
print('Test')

test.plot()
test1.plot()

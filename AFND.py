import matplotlib.pyplot as plt
from graphviz import Digraph

EPS = 'ε'

class Estado:
    def __init__(self,esFinal):
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
    #El alfabeto puede venir dividido por comas o en un rango separado por un guion, sin espacios en ambos casos.
    def __init__(self,id,alf):
        self.id = id
        self.G = Digraph()
        self.G.attr(rankdir = 'LR')
        self.estados = {}
        self.alf=set()
        #En caso de que sea con comas
        if alf.count(','):
            self.alf= set(alf.split(','))
        else:
            min,max = alf.split('-')
            for i in range(ord(max)+1-ord(min)):
                self.alf.add(chr(ord(min)+i))
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
            if states.final:
                self.G.node(str(origin),shape='doublecircle')
            for simbol,destiny in states.transiciones.items():
                for end in destiny:
                    self.G.edge(str(origin), str(end), label=simbol)
        self.G.render(filename=self.id,view=True,directory='resources', cleanup=False, format='png')

    def getEstados(self):
        return set(self.estados.keys)

    #Regresa los estados alcanzables por transiciones epsilo desde cualquier estado en edos
    def cEpsilon(self, edos, Cerr):
        for estado in edos:
            if (not estado in Cerr) and EPS in self.estados[estado].transiciones:
                for i in self.estados[estado].transiciones[EPS]:
                    Cerr.add(i)
                    Cerr.union(self.cEpsilon({i},Cerr))
        return Cerr

    def mover_A(self,edos,s):
        return edos[s]

    def ir_A(self,edos,s):
        return self.cEpsilon(mover_A(edos,s))

    def opcional(self):# ε
        # Se crean los nuevos estados iniciales y finales
        nInicial = Graph.cNode
        nFinal = Graph.cNode+1
        Graph.cNode+=2
        self.estados[nInicial] = Estado(False)
        self.estados[nFinal] = Estado(True)
        # El nuevo inicial apunta al inicial original y al nuevo final
        self.estados[nInicial].addTransicion(EPS, self.inicial)
        self.estados[nInicial].addTransicion(EPS, nFinal)
        self.estados[self.final].addTransicion(EPS, nFinal)
        self.estados[self.final].final=False
        # Se actualizan los estados iniciales y finales
        self.inicial = nInicial
        self.final = nFinal

    def cerradura_positiva(self):
        # Se crean los nuevos estados iniciales y finales
        nInicial = Graph.cNode
        nFinal = Graph.cNode+1
        Graph.cNode+=2
        self.estados[nInicial] = Estado(False)
        self.estados[nFinal] = Estado(True)
        # El nuevo inicial apunta al inicial original y el final original apunta al inicial original
        self.estados[nInicial].addTransicion(EPS, self.inicial)
        self.estados[self.final].addTransicion(EPS, self.inicial)
        self.estados[self.final].addTransicion(EPS, nFinal)
        self.estados[self.final].final=False
        # Se actualizan los estados iniciales y finales
        self.inicial = nInicial
        self.final = nFinal

    def cerradura_kleene(self):
        # Se crean los nuevos estados iniciales y finales
        nInicial = Graph.cNode
        nFinal = Graph.cNode+1
        Graph.cNode+=2
        self.estados[nInicial] = Estado(False)
        self.estados[nFinal] = Estado(True)
        # El nuevo inicial apunta al inicial original y al nuevo final, y el final original apunta al inicial original
        self.estados[nInicial].addTransicion(EPS, self.inicial)
        self.estados[nInicial].addTransicion(EPS, nFinal)
        self.estados[self.final].addTransicion(EPS, self.inicial)
        self.estados[self.final].addTransicion(EPS, nFinal)
        self.estados[self.final].final=False
        # Se actualizan los estados iniciales y finales
        self.inicial = nInicial
        self.final = nFinal

test = Graph('Opcional','a,b,c')
test.basico('a')
test.opcional()
print(test.cEpsilon(test.estados,set()))
print(test.alf)

# test2 = Graph('CerraduraP','a,b,c')
# test2.basico('b')
# test2.cerradura_positiva()

# test3 = Graph('CerraduraK','a-f')
# test3.basico('c')
# print('alfabeto:',test3.alf)
# test3.cerradura_kleene()

# test.plot()
# test2.plot()
# test3.plot()

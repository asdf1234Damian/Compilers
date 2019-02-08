import matplotlib.pyplot as plt
from graphviz import Digraph
import os
os.environ["PATH"] += os.pathsep + 'C:/Program Files (x86)/Graphviz2.38/bin/'

EPS = 'ε'

class Estado:
    def __init__(self,esFinal):
        self.final = esFinal
        self.transiciones = {}

    def addTransicion(self, simbolo, destino):
        #Checa si el simbolo ya esta en el diccionario antes de hacerle append
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
        self.inicial=None
        self.final=None
        #En caso de que sea con comas
        if len(alf)==1:
            self.alf.add(alf)
            return
        if alf.count(','):
            self.alf= set(alf.split(','))
        else:
            min,max = alf.split('-')
            for i in range(ord(max)+1-ord(min)):
                self.alf.add(chr(ord(min)+i))

    def print(self):
        for origen,destino in self.estados.items():
            print('Origen: ',origen)
            for sim,dest in destino.transiciones.items():
                print(sim,dest)

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
        self.G.clear()
        self.G.attr(rankdir = 'LR')
        for origin,states in self.estados.items():
            if states.final:
                self.G.node(str(origin),shape='doublecircle')
            for simbol,destiny in states.transiciones.items():
                for end in set(destiny):
                    self.G.edge(str(origin), str(end), label=simbol)
        self.G.node('S', label=None, shape='point')
        self.G.edge('S',str(self.inicial))
        self.G.render(filename=self.id,view=True,directory='resources', cleanup=False, format='png')

    def getEstados(self):
        return set(self.estados.keys)

    #Regresa los estados alcanzables por transiciones epsilon desde cualquier estado en edos
    def cEpsilon(self, edos, Cerr):
        stack = []
        if isinstance(edos,int):
            stack.append(edos)
        else:
            stack = list(edos)

        while len(stack)!=0:
            edo = stack[0]
            del stack[0]
            if (not (edo in Cerr)) and EPS in self.estados[edo].transiciones:
                Cerr.add(edo)
                for i in self.estados[edo].transiciones[EPS]:
                    stack.append(i)
                    Cerr.union(self.cEpsilon(i,Cerr))
                    Cerr.add(i)
            # print(edos)
        return Cerr

    def moverA(self,edos,s):#edos debe ser un set o lista
        list(edos)
        for edo in edos:
            if s in edo.transiciones.key():
                for i in edo.transiciones[s]:
                    edos.append(i)

    def irA(self,edos,s):
        return self.cEpsilon(moverA(edos,s),set({}))

    #def pertenece(this):
    def pertenece(this):#TODO
        bool(len(set(this.final).intersection(c)))

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

    def concat(self, f2):
        #Se copian todos los estados con sus transiciones
        for key,value in f2.estados.items():
            self.estados[key] = value
        #Se copian el alfabeto
        self.alf.union(f2.alf)
        #Los concatena y se elimina el estado sobrante de f2
        self.estados.pop(f2.inicial,None)
        for key, val in f2.estados[f2.inicial].transiciones.items():
            for dest in val:
                self.estados[self.final].addTransicion(key,dest)
        #Cambia los estados finales e iniciales
        self.estados[self.final].final=False
        self.final = f2.final


    def unir(self,f2):
        #Se copian todos los estados con sus transiciones
        for key,value in f2.estados.items():
            self.estados[key] = value
        #Se copian el alfabeto
        self.alf.union(f2.alf)
        # Se crean los nuevos estados iniciales y finales
        nInicial = Graph.cNode
        nFinal = Graph.cNode+1
        Graph.cNode+=2
        self.estados[nInicial] = Estado(False)
        self.estados[nFinal] = Estado(True)
        #Se unen a los dos automatas con los nuevso estados
        self.estados[nInicial].addTransicion(EPS,self.inicial)
        self.estados[nInicial].addTransicion(EPS,f2.inicial)
        self.estados[self.final].addTransicion(EPS,nFinal)
        self.estados[f2.final].addTransicion(EPS,nFinal)
        #Cambia los estados finales e iniciales
        self.estados[f2.final].final=False
        self.estados[self.final].final=False
        #se actualizan los estados finales e inciales
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
        


f1 = Graph('F1','a')
f1.basico('a')
f1.opcional()

f2 = Graph('F2','b')
f2.basico('b')
f2.cerradura_positiva()

f3 = Graph('f3', 'c')
f3.basico('c')
f2.unir(f3)

f1.concat(f2)

f4 = Graph('f4', 'd')
f4.basico('d')
f4.cerradura_kleene()
f4.plot()

f1.concat(f4)
f1.plot()
print(f1.cEpsilon(f1.inicial,set()))
#TODO fix from here
#

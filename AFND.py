import matplotlib.pyplot as plt
import glob
from graphviz import Digraph
import os
os.environ["PATH"] += os.pathsep + 'C:/Program Files (x86)/Graphviz2.38/bin/'

EPS = 'ε'

def delImages():
    files = glob.glob('images/*')
    for f in files:
        os.remove(f)

class Transicion: 
    def __init__(self, simbolos, destinos):
        self.simbolos = simbolos
        self.destinos = [destinos]
    
class Estado:
    def __init__(self, esFinal):
        self.final = esFinal
        self.transiciones = {}

    def addTransicion(self,exp,simb,dest):
        if exp in self.transiciones.keys():
            self.transiciones[exp].destinos.append(dest)
        else:
            self.transiciones[exp] = Transicion(simb,dest)

    def addEpsTrans(self,dest):
        self.addTransicion(EPS,{EPS},dest)

class Automata:
    nxtNode = 0
    # El alfabeto puede venir dividido por comas o en un rango separado por un guion, sin espacios en ambos casos.
    def __init__(self, exp):
        self.exp  = exp
        self.G = Digraph()
        self.estados = {}  # Enteros
        self.alf = set()
        if len(exp)==0:
            self.inicial = None
            self.final = None
            return
        self.inicial = Automata.nxtNode
        self.final = Automata.nxtNode+1
        self.estados[self.inicial] = Estado(False)
        self.estados[self.final] = Estado(True)
        Automata.nxtNode += 2
        if len(exp) == 1 :
            self.alf = {exp}
        else:
            if exp.count('-'):
                inicio, fin = [ord(x) for x in exp.split('-')]
                for simb in range(inicio,fin+1):
                    self.alf.add(chr(simb))
            else:
                self.alf = set(exp.split(','))
        self.estados[self.inicial].addTransicion(exp,self.alf,self.final)


    def print(self):
        for origen, destino in self.estados.items():
            print('Origen: ', origen)
            for exp, trns in destino.transiciones.items():
                print('\t', exp, ':= {', ','.join(
                    trns.simbolos), '} ->', trns.destinos, sep='')

    def crearDeTablas(self, path):
        #La primer linea del archivo es el alfabeto
        # self.exp=path[:-4]
        f = open(path, "r").readlines()
        self. alf = f[0].replace('\n','').split(',')
        # El estado inicial esta en la linea 2 en la segunda posicion
        self.inicial = f[1].replace('\n', '').split()[1]
        #las lineas de 1 en adelante son los estados y transicones
        for linea in f[1:]:
            linea = linea.replace('\n','').split()
            #El primer elemento de la linea es el tipo ((T)erminal/(N)o terminal)
            #Se compara a 'T' para convertirlo a booleano
            terminal = linea[0] == 'T'
            # El segundo es el nombre del estado o nodo
            nodeName = linea[1] 
            #Crea el estado
            self.estados[nodeName] = Estado(terminal)
            for i in range(len(self.alf)):
                if linea[i+2] != '-':
                    simb = self.alf[i]
                    fin = 'S'+linea[i+2]
                    self.estados[nodeName].addTransicion(simb,simb,fin)

    def plot(self,id):
        self.G.clear()
        #Esto se cambia para cambiar el tamaño de la imagen 
        self.G.attr(ratio='fill', size='3.8,2.77',
                    dpi='300', rank='same', rankdir='LR')
        self.G.edge('S', str(self.inicial))
        for origin,dest in self.estados.items():
            if self.estados[origin].final:
                self.G.node(str(origin), shape='doublecircle')
            for exp, trns in dest.transiciones.items():
                for dest in trns.destinos:
                    self.G.edge(str(origin), str(dest), label=exp)
        self.G.node('S', label=None, shape='point', )
        self.G.render(filename=id, view=False,
                      directory='images', cleanup=True, format='png')

    # Regresa los estados alcanzables por transiciones epsilon desde cualquier estado en edos
    def cEpsilon(self,edos):
        res = []
        i = 0 
        while i != len(edos):
            edo = self.estados[edos[i]]
            if EPS in edo.transiciones.keys():
                for d in edo.transiciones[EPS].destinos:
                    if not d in edos:
                        edos.append(d)
                        res.append(d)
            res.append(edos[i])
            i+=1
        return res



    def moverA(self, edos, s):  # edos debe ser un set o lista
        stack = []
        result = set()
        stack = list(edos)
        for edo in stack:
            if edo in self.estados.keys():
                for tr in self.estados[edo].transiciones.values():
                    if s in tr.simbolos:
                        result = result.union(set(tr.destinos))
        return list(result)

    def irA(self, edos, s):
        return self.cEpsilon(self.moverA(edos, s))

    def pertenece(self, sigma):
        edos = [self.inicial]
        for s in sigma:
            edos = self.irA(self.cEpsilon(edos), s)
            if (len(edos)==0):
                return False
        if self.final in edos:
            return True
        return False

    def opcional(self):  # ε
        # Se crean los nuevos estados iniciales y finales
        self.exp ='('+self.exp+')' '+eps'
        nInicial = Automata.nxtNode
        nFinal = Automata.nxtNode + 1
        Automata.nxtNode += 2
        self.estados[nInicial] = Estado(False)
        self.estados[nFinal] = Estado(True)
        # El nuevo inicial apunta al inicial original y al nuevo final
        self.estados[nInicial].addEpsTrans(self.inicial)
        self.estados[nInicial].addEpsTrans(nFinal)
        self.estados[self.final].addEpsTrans(nFinal)
        self.estados[self.final].final = False
        # Se actualizan los estados iniciales y finales
        self.inicial = nInicial
        self.final = nFinal

    def concat(self, f2):
        self.exp = '('+self.exp+')'+f2.exp
        # Se copian todos los estados con sus transiciones
        self.estados.update(f2.estados)
        # Se copian el alfabeto
        self.alf = self.alf.union(f2.alf)
        # Los concatena y se elimina el estado sobrante de f2
        self.estados.pop(f2.inicial, None)
        self.estados[self.final].transiciones.update(
            f2.estados[f2.inicial].transiciones)
        # Cambia los estados finales e iniciales
        self.estados[self.final].final = False
        self.final = f2.final

    def unirM(self, *automatas):
        self.exp = ''
        finales = [self.final]
        #Crea el nuevo estado inicial
        nInicial = Automata.nxtNode
        Automata.nxtNode += 1
        self.estados[nInicial] = Estado(False)
        self.estados[nInicial].addEpsTrans(self.inicial)
        self.inicial = nInicial
        #Copia transiciones
        for a in automatas:
            self.exp += automatas.exp
            #Compia los simbolos de todos los automatas
            self.alf = self.alf.union(a.alf)
            #Une el nuevo inicial a todos los otros iniciales
            self.estados[nInicial].addEpsTrans(a.inicial)
            #Copia los estados y transicione
            self.estados[nInicial]
            self.estados.update(a.estados)
            finales.append(a.final)
            self.final=finales

    def unir(self, f2):
        # Se actualiza la expresion
        self.exp = '('+self.exp+')'+'+'+f2.exp
        # Se copian todos los estados con sus transiciones
        self.estados.update(f2.estados)
        # Se copian el alfabeto
        self.alf = self.alf.union(f2.alf)
        # Se crean los nuevos estados iniciales y finales
        nInicial = Automata.nxtNode
        nFinal = Automata.nxtNode + 1
        Automata.nxtNode += 2
        self.estados[nInicial] = Estado(False)
        self.estados[nFinal] = Estado(True)
        # Se unen a los dos automatas con los nuevso estados
        self.estados[nInicial].addEpsTrans(self.inicial)
        self.estados[nInicial].addEpsTrans(f2.inicial)
        self.estados[self.final].addEpsTrans(nFinal)
        self.estados[f2.final].addEpsTrans(nFinal)
        # Cambia los estados finales e iniciales
        self.estados[f2.final].final = False
        self.estados[self.final].final = False
        # se actualizan los estados finales e inciales
        self.inicial = nInicial
        self.final = nFinal

    def cerradura_positiva(self):
        # Se crean los nuevos estados iniciales y finales
        self.exp='('+self.exp+')^+'
        nInicial = Automata.nxtNode
        nFinal = Automata.nxtNode + 1
        Automata.nxtNode += 2
        self.estados[nInicial] = Estado(False)
        self.estados[nFinal] = Estado(True)
        # El nuevo inicial apunta al inicial original y el final original apunta al inicial original
        self.estados[nInicial].addEpsTrans(self.inicial)
        self.estados[self.final].addEpsTrans(self.inicial)
        self.estados[self.final].addEpsTrans(nFinal)
        self.estados[self.final].final = False
        # Se actualizan los estados iniciales y finales
        self.inicial = nInicial
        self.final = nFinal

    def cerradura_kleene(self):
        self.exp += '^k'
        # Se crean los nuevos estados iniciales y finales
        nInicial = Automata.nxtNode
        nFinal = Automata.nxtNode + 1
        Automata.nxtNode += 2
        self.estados[nInicial] = Estado(False)
        self.estados[nFinal] = Estado(True)
        # El nuevo inicial apunta al inicial original y al nuevo final, y el final original apunta al inicial original
        self.estados[nInicial].addEpsTrans(self.inicial)
        self.estados[nInicial].addEpsTrans(nFinal)
        self.estados[self.final].addEpsTrans(self.inicial)
        self.estados[self.final].addEpsTrans(nFinal)
        self.estados[self.final].final = False
        # Se actualizan los estados iniciales y finales
        self.inicial = nInicial
        self.final = nFinal

    def conversion_A_Archivo(self, path):
        if isinstance(self.final,int):
            self.final = {self.final}
        with open(path, "w") as file:
            #Inicializa la tabla y el indice para recorrerla
            S = [self.cEpsilon([self.inicial])]
            currS = 0
            #Imprime el alfabeto primero 
            file.writelines(','.join(self.alf)+'\n')
            #Mientras no haya llegado al ultimo estado
            while currS != len(S):
                #Guarda el nuevo estado
                si = S[currS]
                #Se imprime el nombre del nuevo estado
                file.write('S'+str(currS)+' ')
                #Sj es el resultado de irA de si con
                #cada simbolo del alfabeto
                for simb in self.alf:
                    sj = self.irA(si,simb)
                    #Se guarda sj en caso de que no este y despues se 
                    #imprime el indice respectivo
                    if len(sj):
                        if not sj in S:
                            S.append(sj)
                        file.write(str(S.index(sj))+' ')
                    else:#Si no, si no tiene transicion a sj
                        file.writelines('- ')
                if set(si).intersection(self.final):
                    file.writelines(str((currS+1)*10)+'\n')
                else:
                    file.write('-1')
                currS += 1
        self = Automata('')
        self.crearDeTablas(path)

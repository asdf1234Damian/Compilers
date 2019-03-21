import itertools
EPS = 'ε'

#Funcion para eliminar repeticiones sin usar set
def delRep(l):
	l = list(l)
	l.sort()
	return list(l for l,_ in itertools.groupby(l))

class Gramatica:
	def __init__(self, path):
		self.reglas = {}
		self.terminales = set()
		self.noTerminales = set()
		self.raiz = None
		#Crea el diccionario de reglas segun el archivo
		with open(path, "r") as file:
			file = file.readlines()
			# El estado incial es el primer elemento en la primer linea
			self.raiz = file[0].split()[0]
			#Set con todos los simbolos en la gramatica, terminales y no terminales
			simbolos = set()
			# Se guardan todas las reglas en un mapa
			for line in file:
				line = line.split()
				#Se borra la flecha de la tabla
				del line[1]
				simbolos.update(set(line))
				izq = line[0]
				self.noTerminales.add(izq)
				der = line[1:]
				if izq in self.reglas.keys():
					self.reglas[izq].append(der)
				else:
					self.reglas[izq] = [der]
			#Se calcula terminales
			self.terminales = simbolos - self.noTerminales
			if not EPS in self.terminales:
				self.terminales.add(EPS)
			self.terminales = delRep(self.terminales)
			self.noTerminales = delRep(self.noTerminales)


	def print(self):
		# print('Raiz:', self.raiz)
		# print('Vt:', self.terminales)
		# print('Vn:', self.noTerminales)
		print(''.rjust(50,'-'))
		for izq,derArr in self.reglas.items():
			for der in derArr:
				print(izq, der )
		print(''.rjust(50,'-'))

	def first(self, simb):
		# res será el resultado
		res = []
        # Se limpia la entrada
		if isinstance(simb, str):
			simb = list(simb.split())
		if EPS in simb:
			res.append(EPS)
			simb.remove(EPS)
		# Mientras simb tenga un elementos (despues de borrar eps)
		if len(simb):
            # Si encuentra un terminal, regresa el resultado
			if simb[0] in self.terminales:
				res.append(simb[0])
				return delRep(res)
            # Si no, busca las reglas donde el simbolo esta en la izq
			for der in self.reglas[simb[0]]:
				res += self.first(der + simb[1:])
		return delRep(res)


	# alpha - > gamma A beta
	def follow(self, A, stack =[]):
		fllwA = []
		if A in stack:
			stack=[]
			return delRep(fllwA)
		stack.append(A)
		if A == self.raiz:
			fllwA.append('$')
		for alpha, derArr in self.reglas.items():
			for der in derArr:
				if A in der:
					i = der.index(A)
					beta=der[i+1:]
					if len(beta):
						frstB = self.first(beta)
						fllwA += frstB
						if EPS in frstB:
							fllwA += self.follow(alpha,stack)
					else:
						fllwA += self.follow(alpha,stack)
		stack=[]
		return delRep(fllwA)





g  = Gramatica('testFiles/Gramatica.txt')
print(g.first('E'))
print(g.follow('F'))

import itertools
EPS = 'ε'

#Funcion para eliminar repeticiones sin usar set
def delRep(l):
	l = list(l)
	l.sort()
	return list(l for l,_ in itertools.groupby(l))

class Gramatica:
	def __init__(self, path):
		self.tabla = {}
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
			self.terminales.add('$')
			self.terminales = delRep(self.terminales)
			self.noTerminales = delRep(self.noTerminales)
			self.genTabla()


	def print(self):
		print('Raiz:', self.raiz)
		print('Vt:', self.terminales)
		print('Vn:', self.noTerminales)
		print(''.rjust(50,'-'))
		for izq,derArr in self.reglas.items():
			for der in derArr:
				print(izq, der )
		print(''.rjust(50,'-'))
		terminales = self.terminales[:]
		terminales.remove(EPS)
		terminales.append('$')
		print(''.center(6),'|',end = '')
		for t in terminales:
			print(t.center(6),'|',end = '')
		print()
		for x in self.noTerminales:
			print('-'*8*(len(terminales)+1))
			print(x.center(6),'|',end = '')
			for y in terminales:
				print((''.join(self.tabla[x][y][:-1])).center(6),'|',end = '')
			print()

	def first(self, simb,getDer):
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
				f = self.first(der+simb[1:],False)
				res+=f
		return res


	# alpha - > gamma A beta
	# Hay que mandar a llamar con una lista vacia en stack
	def follow(self, A, stack =[]):
		fllwA = []
		if A in stack:
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
						frstB = self.first(beta,False)
						fllwA += frstB
						if EPS in frstB:
							fllwA += self.follow(alpha,stack[:])
					else:
						fllwA += self.follow(alpha,stack[:])
		return delRep(fllwA)


	def genTabla(self):
		terminales = self.terminales[:]
		terminales.remove(EPS)
		terminales.append('$')
		self.tabla = {n : {t : [] for t in terminales} for n in self.noTerminales}
		i = 0
		for izq, derArr in self.reglas.items():
			for der in derArr:
				i+=1
				if EPS in der:
					f = self.follow(izq)
				else:
					f = self.first(der[:],True)
				for s in f:
					self.tabla[izq][s] = (der[:]+[','+str(i)])

	def analyze(self, cad):
		cad =cad+'$'
		stack = ['$', self.raiz]
		print('-'*85)
		print('|','Analisis lexico'.center(81),'|')
		print('-'*85)
		while len(stack) and len(cad):
			print((' '.join(stack)).ljust(30),end='| ')
			print((' '.join(cad)).ljust(50),'|')
			sp = stack.pop()
			simb  = cad [0]
			if sp == EPS:
				pass
			elif (sp in self.terminales):
				if simb == sp:
					if simb == '$':
						return True
					cad = cad[1:]
				else:
					return False
			else:
				if not simb in self.terminales:
					return False
				contTabla  = self.tabla[sp][simb][:-1]
				if(len(contTabla)):
					stack += contTabla[::-1]
				else:
					return False
		return False




g  = Gramatica('testFiles/Gramatica.txt')
<<<<<<< HEAD
print(g.first('E'))
print(g.follow('F'))
=======
g.print()
print(g.analyze('n+n*(n-n)'))
>>>>>>> 9632ce8578b9966b72df466b30498785df36d0ed

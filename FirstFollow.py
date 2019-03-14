class Gramatica:
	def __init__(self, path):
		self.reglas = {}
		self.terminales = set()
		self.noTerminales = set()
		self.raiz = None
		#Crea el diccionario de reglas segun el archivo
		with open(path, "r") as file:
			file = file.readlines()	
			# El estado inciial es el primer elemento en la primer linea
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
			self.terminales = simbolos - self.noTerminales
			# print('Raiz', self.raiz)
			# print('Terminales',self.terminales)
			# print('No Terminales', self.noTerminales)
			# print('Reglas')
			# for r in self.reglas.keys():
			# 	for i in self.reglas[r]:
			# 		print(r,'->' ,''.join(i))

	def first(self, izq):
		# Si es terminal, solo lo regresa
		if izq in self.terminales:
			return izq
		else:
			#Se guardan en orig todos los lados izq donde en la derecha se encuentra izq 
			orig = []
			for k in self.reglas.keys():
				for der in self.reglas[k]:
					if izq in der and izq not in orig:
						orig.append(k)
			#Se hace first recursivamente a todas las reglas guardadas en orig
			res = []
			for o in orig:
				for der in self.reglas[o]:
					f = self.first(der[0])
					res.append(f)
			# Se eliminan las repeticiones con set() y se regresa como lista 
		return list(set(res))

	
			



g  = Gramatica('testFiles/Gramatica.txt')
print(g.first('E'))


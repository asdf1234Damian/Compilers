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
		#res será el resultado 
		res = []
		#En orig se guardan todos los no terminales de izq
		orig = []
		for noTer in izq.split():
			orig.append(noTer)
		
		#Si es terminal diferente de epsilon, regresa el elemento
		if orig[0] in self.terminales and orig[0] != 'eps':
			res.append(orig[0])
			return res
		
		#Si es epsilon
		elif orig[0] == 'eps':
			#Si solamente es epsilon, se regresa 
			if len(orig) < 2:
				res.append(orig[0])
				return res
			#Si tiene algún no terminal a la derecha se regresa el first del no terminal y epsilon
			else:
				f = self.first(orig[1])
				for sim in f:
					res.append(sim)
				res.append('eps')
				return res

		#En caso de que sea un no terminal
		else:
			#Cadena auxiliar que se mandara como argumento a first() 
			cad_aux = ''
			#Ladoe derechos de las reglas de produccion del primer no terminal 
			der = self.reglas[orig[0]]
			for reg in der:
				#Se pasan a cadena las reglas del lado derecho
				for i in reg:	
					cad_aux += i
					cad_aux +=' '
				j = 1
				#Se concatenan a cad_aux los no terminales que queden en orig
				while j < len(orig):
					cad_aux += orig[j]
					cad_aux += ' '
					j += 1
				#Se obtiene el first de la cadena
				f = self.first(cad_aux)
				#Si f consta de mas elementos que 1
				if len(f) > 1:
					for sim in f:
						res.append(sim)
				else:
					res.append(f[0])
				cad_aux = ''
			#Se eliminan simbolos iguales con set y se mandan en una lista
			return list(set(res))
			

	def follow(self, noTerminal):
		#if 
		follow = set()
		aux = set()
		stackFollows = []
		if noTerminal == self.raiz:
			follow.add('ε')
		else:
			for izq, der in self.reglas.items():
				for reg in der:
					if noTerminal in reg:
						aux.add(izq)
			#print(aux)
			"""for noTer in aux:
				for reg in self.reglas[noTer]:
					print(reg)
					i = 0
					while i<len(reg):
						if reg[i] == noTerminal:
							print(reg[i])
							if reg[i+1] != '\0':
								print(reg[i+1])
								follow.add(self.first(reg[i+1]))
								print(follow)
								if 'ε' in self.first(reg[i+1]):
									stackFollows.add(noTer)
									if stackFollows[-1] != stackFollows[-2]: 
										self.follow(noTer)
									else:
										stackFollows.pop()
							else:
								stackFollows.add(noTer)
								if stackFollows[-1] != stackFollows[-2]: 
									self.follow(noTer)
						i += 1
			print(follow)"""





g  = Gramatica('testFiles/Gramatica.txt')
print(g.first('Ep Tp'))
g.follow('T')

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
			if not 'eps' in self.terminales:
				self.terminales.add('eps')
			# print('Raiz', self.raiz)
			# print('Terminales',self.terminales)
			# print('No Terminales', self.noTerminales)
			# print('Reglas')
			# for r in self.reglas.keys():
			# 	for i in self.reglas[r]:
			# 		print(r,'->' ,''.join(i))

	def first(self, simb):
        # res será el resultado
        res = []
        # Se limpia la entrada
        if isinstance(simb, str):
            simb = list(set(simb.split()))
        if 'eps' in simb:
            res.append('eps')
            simb.remove('eps')
        # Mientras simb tenga un elementos (despues de borrar eps)
        if len(simb):
            # Si encuentra un terminal, regresa el resultado
            if simb[0] in self.terminales:
                res.append(simb[0])
                return res
            # Si no, busca las reglas donde el simbolo esta en la izq
            for der in self.reglas[simb[0]]:
                res += self.first(der + simb[1:])
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

def readAFD(path):
	tab = []
	aux = []
	cont = 0
	flag = 0
	with open(path, "r") as file:
		#Se obtienen todas la lineas del archivo
		for line in file:
			#Se obtiene cada caracter de cada linea
			for l in line:
				#Se eliminan los caracteres inecesarios
				if l != '\n' and l != ' ' and l != ',':
					if len(tab) == 0:
						aux.append(l)
					elif l != 'S': 
						if l == '-':
							aux_c = l
							flag = 1
						if flag == 0:
							aux.append(l)
						if flag == 1 and l != '-':
							aux_c += l
							aux.append(aux_c)
							flag = 0 
							aux_c = ''
			if len(tab) != 0:
				#Se quita el caracter que indica a que estado corresponde la transición
				#aux.pop(0)
				#Se unen los caracteres que indican el token
				aux_c = ''
				while len(aux) > len(tab[0])+1:
					aux_c = aux_c + aux.pop(len(tab[0])+1)
				aux.append(aux_c)
			#Se agrega la lista a la tabla
			tab.append(aux.copy())
			aux.clear()
	return tab

def readText(path):
	txt = []
	with open(path, "r") as file:
		for line in file:
			for l in line:
				txt.append(l)
	return txt

class Lexic:
	def __init__(self, tabla, txt):
		self.tabla = tabla
		self.txt = txt
		self.iniLex = 0
		self.indAct = 0
		self.finLex = 0
		self.estadoAct = 0

	def getToken(self):
		aux = 0
		ind_c = 0
		token = -1
		est = 0
		#Se indica el inicio del lexema con la posición actual de la cadena a analizar
		self.iniLex = self.estadoAct
		self.finLex = 0
		while token == -1 or self.finLex == 0:
			#Cuando se llegue al final de la cadena
			if self.indAct >= len(self.txt):
				break
			#Se obtiene el caracter que sigue en la cadena
			c = self.txt[self.indAct]
			for alf in self.tabla[0]:
				#Si el caracter se encuentra en el alfabeto
				if c == alf:
					print("estado: "+str(self.estadoAct))
					#Se obtiene el indice de la tabla donde se encuentra el caracter
					ind_c = self.tabla[0].index(c)
					for col in self.tabla:
						#Se compara el estado actual con los estados en la tabla
						if col[0] == str(self.estadoAct): 
							#Se obtiene el token correspondiente al estado
							token = int(col[len(col)-1])
							print("token: " + str(token))
							#Se obtiene el estado al que se pasará
							est = int(col[ind_c + 1])
							if est == -1:
								finLex = 1
					#Se cambia el valor del estado en que nos encontramos
					if est != -1:
						self.estadoAct = est
			#Si el caracter que sigue no se encuentra en la tabla
			if not c in self.tabla[0]:
				finLex = 1
			#Se incrementa el índice del caracter a analizar en la cadena
			self.indAct += 1
			print("\n")
		return token

	def returnToken(self):
		self.indAct = self.iniLex
		self.estadoAct = 0
		"""#Se obtiene el caracter que sigue en la cadena
		c = self.txt[self.indAct]
		for alf in self.tabla[0]:
			#Si el caracter se encuentra en el alfabeto
			if c == alf:"""

	def getLexema(self):
		lex = ''
		for i in range(self.iniLex, self.indAct - 1):
			lex += self.txt[i]
		return lex
	

t = readAFD("tab.txt")			
print(t)		
l = Lexic(t, readText("p.txt"))
print(l.txt)
l.getToken()
print("get: "+str(l.indAct))
l.returnToken()
print("return: "+str(l.indAct))
l.getToken()
print("get :"+str(l.indAct))
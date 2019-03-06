class Lexic:
	def __init__(self, tab_path, txt_path):
		#Inicializacion
		#Estas variables NO dependen de los argumentos del constructor
		self.indAct = 0 #Indice Actual
		self.iniLex = 0 #Inicio del lexema
		self.finLex = 0 #Fin del lexema
		self.estadoAct = 0 #Estado Actual
		# Se recuperan la tabla y el alfabeto del archivo tab_path
		self.tab = []
		self.alf = []
			#Se obtienen todas la lineas del archivo
		with open(tab_path, "r") as file:
			#Se convierte en un arreglo de lineas en vez de un archivo
			file = file.readlines()
			#La primer linea es el alfabeto separado por espacios
			self.alph = file[0].split()
			#A partir de la segunda linea ([1:]) son las transiciones
			for line in file[1:]:
				# Se separa por espacios y se omite el primer elemento y se guarda en el auxiliar
				self.tab.append(line.split()[1:])
		# Se recupera el texto del archivo txt
		self.txt = []
		with open(txt_path, "r") as file:
			for line in file:
				self.txt += (list(line))	

	def getToken(self):
		aux = 0
		ind_c = 0
		token = -1
		est = 0
		#Se indica el inicio del lexema con la posición actual de la cadena a analizar
		self.iniLex = self.indAct
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
					#print("estado: "+str(self.estadoAct))
					#Se obtiene el indice de la tabla donde se encuentra el caracter
					ind_c = self.tabla[0].index(c)
					for e in self.tabla:
						#Se compara el estado actual con los estados en la tabla
						if e[0] == str(self.estadoAct): 
							#Se obtiene el estado al que se pasará
							est = int(e[ind_c + 1])
							#Se obtiene el token correspondiente al estado
							token = int(self.tabla[est+1][-1])
							if est == -1 or token!=-1:
								self.finLex = 1
					#Se cambia el valor del estado en que nos encontramos
					if est != -1:
						self.estadoAct = est
			#Se incrementa el índice del caracter a analizar en la cadena
			self.indAct += 1
			#Si el caracter que sigue no se encuentra en la tabla
			if not c in self.tabla[0]:
				finLex = 1
		self.estadoAct = 0
		return token

	def returnToken(self):
		self.indAct = self.iniLex
		self.estadoAct = 0
		
	def getLexema(self):
		return self.txt[self.indAct - 1]

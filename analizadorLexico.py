class Lexic:
	def __init__(self, tab_path):
		#Inicializacion
		#Estas variables NO dependen de los argumentos del constructor
		self.indAct = 0  # Indice Actual
		self.iniLex = 0  # Inicio del lexema
		# Se recuperan la tabla y el alfabeto del archivo tab_path
		self.tab = []
		self.alf = []
		#Se obtienen todas la lineas del archivo
		with open(tab_path, "r") as file:
			#Se convierte en un arreglo de lineas en vez de un archivo
			file = file.readlines()
			#La primer linea es el alfabeto separado por espacios
			self.alf = file[0].split()
			#A partir de la segunda linea ([1:]) son las transiciones
			for line in file[1:]:
				# Se separa por espacios y se omite el primer elemento y se guarda en el auxiliar
				self.tab.append(line.split()[1:])
		# Se recupera el texto del archivo txt
		self.txt = []

	def loadString(self,strng):
		self.txt = strng
		self.indAct = 0  # Indice Actual
		self.iniLex = 0  # Inicio del lexema

	def getToken(self):
		estadoAct = 0
		token = -1
		existTrans = True
		#Se indica el inicio del lexema con la posición actual de la cadena a analizar
		self.iniLex = self.indAct
		while existTrans:
			#Cuando se llegue al final de la cadena
			if self.indAct >= len(self.txt):
				return token
			#Se obtiene el caracter que sigue en la cadena
			c = self.txt[self.indAct]
			#Si el caracter se encuentra en el alfabeto
			if c in self.alf:
				#Se obtiene el indice de la tabla donde se encuentra el caracter
				indice = self.alf.index(c)
				#Se cambia el valor del estado en que nos encontramos
				estadoAct = int(self.tab[estadoAct][indice])
				#Se obtiene el token correspondiente al estado
				if estadoAct != -1:
					token = int(self.tab[estadoAct][-1])
					self.indAct += 1
				else:
					existTrans = False
			#Si el caracter que sigue no se encuentra en la tabla
			else:
				existTrans = False
			#Se incrementa el índice del caracter a analizar en la cadena
		return token

	def returnToken(self):
		self.indAct = self.iniLex

	def getLexema(self):
		return ''.join(self.txt[self.iniLex:self.indAct])

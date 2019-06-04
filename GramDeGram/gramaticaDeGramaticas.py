from analizadorLexico import Lexic
import math

"""
Lista de tokens correspondientes:
símbolo			90	60
->				80	70
OR				70	80
;				40	30
"""

#gram = []

class Gramatica:
	

	def __init__(self):
		self.lexer = Lexic("Automata_Gramaticas.txt")
		self.lexer.changeTxt("[E]->[T][F];[F]->[+][T][F]OR[-][T][F]OR[eps];")
		self.tabla = []
		self.lista = []

	def G(self):
		if self.ListaReglas():
			return True
		return False

	def ListaReglas(self):
		if self.Regla():
			tok = self.lexer.getToken()
			if tok == 40:
				self.tabla.append(self.lista.copy())
				self.lista.clear()
				edoScanner = self.lexer.getEdo()
				if self.ListaReglas():
					return True
				self.lexer.setEdo(edoScanner)
				return True
		return False;

	def Regla(self):
		if self.LadoIzquierdo():
			tok = self.lexer.getToken()
			if tok == 80:
				if self.ListaLadosDerechos():
					return True
		return False

	def LadoIzquierdo(self):
		tok = self.lexer.getToken()
		if tok == 90:
			self.lista.append(self.lexer.getLexema()[1])
			return True
		return False

	def ListaLadosDerechos(self):
		if self.LadoDerecho():
			tok = self.lexer.getToken()
			if tok == 70:
				#self.lista.append('|')
				self.tabla.append(self.lista.copy())
				aux=self.lista[0]
				self.lista.clear()
				self.lista.append(aux)
				if self.ListaLadosDerechos():
					return True
				return False
			self.lexer.returnToken()
			return True
		return False

	def LadoDerecho(self):
		if self.ListaSimbolos():
			return True
		return False

	def ListaSimbolos(self):
		tok = self.lexer.getToken()
		if tok == 90:
			lexema = self.lexer.getLexema()
			if(lexema != "[eps]"):
				self.lista.append(lexema[1])
			else:
				self.lista.append(lexema[1:4])
			if self.ListaSimbolos():
				return True
			return True
		self.lexer.returnToken();
		return False

	def toFile(self):
		f = open("gramatica.txt", 'w')
		for lista in self.tabla:
			regla = " ".join(str(lista[x]) for x in range(1,len(lista)))
			f.write(str(lista[0])+' -> '+regla+'\n')
		f.close()

gram = Gramatica()
if gram.G():
	print("La gramática es correcta")
	gram.toFile()
else:
	print("Error en la gramática")
		
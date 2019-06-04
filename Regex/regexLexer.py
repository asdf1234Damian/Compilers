from analizadorLexico import Lexic
from AFND import Automata
import math

SIMB   = 20
PAR_IZ = 30
CERKLE = 40
CONCAT = 50
CEROPC = 60
PAR_DE = 70
CERPOS = 80
UNION  = 90
RANG   = 120
CONJ   = 130

class regexLexer:
	def __init__(self):
		#Objeto lex de la clase Lexic
		self.lx = Lexic("resources/expAutomata.txt")
		self.f = []

	def anlaisisLex(self,cadena):
		self.lx.loadString(cadena)
		if(self.E(self.f)):
			self.f = self.f[0]
			self.f.conversion_A_Archivo('cache/lexerOutput.txt')
			return True
		return False

	def E(self, f):
		if self.T(f):
			if self.Ep(f):
				return True
		return False

	def Ep(self,f):
		tok = self.lx.getToken()
		if tok == UNION:
			if self.T(f):
				print(self.f)
				f[0].unir(f[1])
				f.pop()
				if self.Ep(f):
					return True
			return False
		self.lx.returnToken()
		return True


	def T(self, f):
		if self.C(f):
			if self.Tp(f):
				return True
		return False

	def Tp(self, f):
		tok = self.lx.getToken()
		if tok == CONCAT:
			if (self.C(f)):
				f[0].concat(f[1])
				f.pop()
				if self.Tp(f):
					return True
			return False
		self.lx.returnToken()
		return True

	def C(self,f):
		if self.F(f):
			if self.Cp(f):
				return True
		return False

	def Cp(self,f):
		tok = self.lx.getToken()
		if tok == CERKLE:
			f[0].cerradura_kleene()
		elif tok == CERPOS:
			f[0].cerradura_positiva()
		elif tok == CEROPC:
			f[0].opcional()
		else:
			self.lx.returnToken()
			return True
		if self.Cp(f):
			return True
		else:
			return False

	def F(self,f):
		tok = self.lx.getToken()
		if tok == PAR_IZ:
			if self.E(f):
				tok = self.lx.getToken()
				if tok == PAR_DE:
					return True
			return False
		elif tok == SIMB or tok == CONJ or tok == RANG:
			lexema = self.lx.getLexema()
			f.append(Automata(lexema))
			return True
		return False

test = regexLexer()

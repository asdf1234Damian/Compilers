from analizadorLexico import Lexic
import AFND
import math

SIMB   = 20
CONCAT = 30
CERPOS = 40
CEROPC = 50
PAR_IZ = 60
PAR_DE = 70
UNION  = 80
CERKLE = 90
CONJ   = 120
RANG   = 130

class regexLexer:
	def __init__(self):
		#Objeto lex de la clase Lexic
		self.lx = Lexic("resources/expAutomata.txt")
		self.f = []

	def anlaisisLex(self,cadena):
		self.f = []
		self.lx.loadString(cadena)
		if(self.E(self.f)):
			self.f = self.f[0]
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
			f.append(AFND.Automata(lexema))
			return True
		return False

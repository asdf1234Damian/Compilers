from  .analizadorLexico import Lexic
import math

#NOTA: Las operaciones son realizadas en radianes
"""
Lista de tokens correspondientes:
+	120
-	70
*	140
/	110
^	130
(	80
)	40
num	20, 220
sin	230
cos 240
tan	260
ln	190
log	250
exp 270
"""
#Alvaro estuvo aqui
#Hola Lolita
#Objeto lex de la clase Lexic
class Calculadora:
	def __init__(self):
		self.lexer = Lexic("Calculadora/tab.txt")
		#Arreglo donde se guardara la evaluacion de la expresion
		self.v = []
		self.infija = []

	def evaluate(self,text):
		self.lexer.changeTxt(text)
		if self.G(self.v):
			inf = ''
			for i in self.infija:
				inf += i
			return self.v[0]
		else:
			return 'Error'

	def G(self,v):
		if self.E(v):
			tok = self.lexer.getToken()
			if tok == -1:
				return True
		return False

	def E(self,v):
		if self.T(v):
			if self.Ep(v):
				return True
		return False

	def Ep(self,v):
		tok = self.lexer.getToken()
		if tok == 120 or tok == 70:
			if tok == 120:
				self.infija.append('+')
			else:
				self.infija.append('-')
			if self.T(v):
				if tok == 120:
					v[-2] = v[-2] + v[-1]
					v.pop()
				else:
					v[-2] = v[-2] - v[-1]
					v.pop()
				if self.Ep(v):
					return True
			return False
		self.lexer.returnToken()
		return True

	def T(self,v):
		if self.P(v):
			if self.Tp(v):
				return True
		return False

	def Tp(self,v):
		tok = self.lexer.getToken()
		if tok == 140 or tok == 110:
			if tok == 140:
				self.infija.append('*')
			else:
				self.infija.append('/')
			if self.P(v):
				if tok == 140:
					v[-2] = v[-2] * v[-1]
					v.pop()
				else:
					v[-2] = v[-2] / v[-1]
					v.pop()
				if self.Tp(v):
					return True
			return False
		self.lexer.returnToken()
		return True

	def P(self,v):
		if self.F(v):
			if self.Pp(v):
				return True
		return False

	def Pp(self,v):
		tok = self.lexer.getToken()
		if tok == 130:
			self.infija.append('^')
			if self.F(v):
				v[-2] = v[-2] ** v[-1]
				v.pop()
				if self.Pp(v):
					return True
			return False
		self.lexer.returnToken()
		return True

	def F(self,v):
		tok = self.lexer.getToken()
		#(E)
		if tok == 80:
			self.infija.append("(")
			if self.E(v):
				tok = self.lexer.getToken()
				self.infija.append(")")
				if tok == 40:
					return True
		#sin(E)
		elif tok == 230:
			tok = self.lexer.getToken()
			if tok == 80:
				self.infija.append("sin(")
				if self.E(v):
					tok = self.lexer.getToken()
					self.infija.append(")")
					if tok == 40:
						v[-1] = math.sin(v[-1])
						return True
			return False
		#cos(E)
		elif tok == 240:
			tok = self.lexer.getToken()
			if tok == 80:
				self.infija.append("cos(")
				if self.E(v):
					tok = self.lexer.getToken()
					self.infija.append(")")
					if tok == 40:
						v[-1] = math.cos(v[-1])
						return True
			return False
		#tan(E)
		elif tok == 260:
			tok = self.lexer.getToken()
			if tok == 80:
				self.infija.append("tan(")
				if E(v):
					tok = self.lexer.getToken()
					self.infija.append(")")
					if tok == 40:
						v[-1] = math.tan(v[-1])
						return True
			return False
		#ln(E)
		elif tok == 190:
			tok = self.lexer.getToken()
			if tok == 80:
				if self.E(v):
					tok = self.lexer.getToken()
					self.infija.append(")")
					if tok == 40:
						v[-1] = math.log10(v[-1])
						return True
			return False
		#log(E)
		elif tok == 250:
			tok = lex.getToken()
			if tok == 80:
				if E(v):
					tok = lex.getToken()
					self.infija.append(")")
					if tok == 40:
						v[-1] = math.log(v[-1])
						return True
		#exp(E)
		elif tok == 270:
			tok = self.lexer.getToken()
			if tok == 80:
				self.infija.append("exp(")
				if self.E(v):
					tok = self.lexer.getToken()
					self.infija.append(")")
					if tok == 40:
						v[-1] = math.exp(v[-1])
						return True
			return False
		#num
		elif tok == 20 or tok == 220:
			car = self.lexer.getLexema()
			v.append(float(car))
			self.infija.append(car)
			return True
		return False

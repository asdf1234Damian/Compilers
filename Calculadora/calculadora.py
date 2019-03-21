import analizadorLexico
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

#Objeto lex de la clase Lexic
lex = analizadorLexico.Lexic("tab.txt", "p.txt")
#Arreglo donde se guardara la evaluacion de la expresion
v = []
infija = []

def G(v):
	if E(v):
		tok = lex.getToken()
		if tok == -1:
			return True
	return False

def E(v):
	if T(v):
		if Ep(v):
			return True
	return False

def Ep(v):
	tok = lex.getToken()
	if tok == 120 or tok == 70:
		if tok == 120:
			infija.append('+')
		else:
			infija.append('-')
		if T(v):
			if tok == 120:
				v[-2] = v[-2] + v[-1]
				v.pop()
			else:
				v[-2] = v[-2] - v[-1]
				v.pop()
			if Ep(v):
				return True
		return False
	lex.returnToken()
	return True

def T(v):
	if P(v):
		if Tp(v):
			return True
	return False

def Tp(v):
	tok = lex.getToken()
	if tok == 140 or tok == 110:
		if tok == 140:
			infija.append('*')
		else:
			infija.append('/')
		if P(v):
			if tok == 140:
				v[-2] = v[-2] * v[-1]
				v.pop()
			else:
				v[-2] = v[-2] / v[-1]
				v.pop()
			if Tp(v):
				return True
		return False
	lex.returnToken()
	return True

def P(v):
	if F(v):
		if Pp(v):
			return True
	return False

def Pp(v):
	tok = lex.getToken()
	if tok == 130:
		infija.append('^')
		if F(v): 
			v[-2] = v[-2] ** v[-1]
			v.pop()
			if Pp(v):
				return True
		return False
	lex.returnToken()
	return True	

def F(v):
	tok = lex.getToken()
	#(E)
	if tok == 80:
		infija.append("(")
		if E(v):
			tok = lex.getToken()
			infija.append(")")
			if tok == 40:
				return True
	#sin(E)
	elif tok == 230:
		tok = lex.getToken()
		if tok == 80:
			infija.append("sin(")
			if E(v):
				tok = lex.getToken()
				infija.append(")")
				if tok == 40:
					v[-1] = math.sin(v[-1])
					return True
		return False
	#cos(E)
	elif tok == 240:
		tok = lex.getToken()
		if tok == 80:
			infija.append("cos(")
			if E(v):
				tok = lex.getToken()
				infija.append(")")
				if tok == 40:
					v[-1] = math.cos(v[-1])
					return True
		return False
	#tan(E)
	elif tok == 260:
		tok = lex.getToken()
		if tok == 80:
			infija.append("tan(")
			if E(v):
				tok = lex.getToken()
				infija.append(")")
				if tok == 40:
					v[-1] = math.tan(v[-1])
					return True
		return False
	#ln(E)
	elif tok == 190:
		tok = lex.getToken()
		if tok == 80:
			if E(v):
				tok = lex.getToken()
				infija.append(")")
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
				infija.append(")")
				if tok == 40:
					v[-1] = math.log(v[-1])
					return True
	#exp(E)
	elif tok == 270:
		tok = lex.getToken()
		if tok == 80:
			infija.append("exp(")
			if E(v):
				tok = lex.getToken()
				infija.append(")")
				if tok == 40:
					v[-1] = math.exp(v[-1])
					return True
		return False
	#num
	elif tok == 20 or tok == 220:
		car = lex.getLexema()
		v.append(float(car))
		infija.append(car)
		return True
	return False

inf = ""
if G(v):
	for i in infija:
		inf += i
	print(inf)
	print(v[0])
else:
	print(False)
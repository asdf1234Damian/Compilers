import analizadorLexico
import math

#NOTA: Las operaciones son realizadas en radianes
"""
Lista de tokens correspondientes:
+	130
-	30
*	80
/	110
^	100
(	90
)	140
num	50
sin	230
cos 250
tan	270
ln	150
log	220
exp 260
"""

#Objeto lex de la clase Lexic
lex = analizadorLexico.Lexic("tab.txt", "p.txt")
#Arreglo donde se guardara la evaluacion de la expresion
v = []

def G(v):
	tok = 0
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
	if tok == 130 or tok == 30:
		if T(v):
			if tok == 130:
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
	if tok == 80 or tok == 110:
		if P(v):
			if tok == 80:
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
	if tok == 100:
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
	if tok == 90:
		if E(v):
			tok = lex.getToken()
			if tok == 140:
				return True
	#sin(E)
	elif tok == 230:
		tok = lex.getToken()
		if tok == 90:
			if E(v):
				tok = lex.getToken()
				if tok == 140:
					v[-1] = math.sin(v[-1])
					return True
		return False
	#cos(E)
	elif tok == 250:
		tok = lex.getToken()
		if tok == 90:
			if E(v):
				tok = lex.getToken()
				if tok == 140:
					v[-1] = math.cos(v[-1])
					return True
		return False
	#tan(E)
	elif tok == 270:
		tok = lex.getToken()
		if tok == 90:
			if E(v):
				tok = lex.getToken()
				if tok == 140:
					v[-1] = math.tan(v[-1])
					return True
		return False
	#ln(E)
	elif tok == 150:
		tok = lex.getToken()
		if tok == 90:
			if E(v):
				tok = lex.getToken()
				if tok == 140:
					v[-1] = math.log10(v[-1])
					return True
		return False
	#log(E)
	elif tok == 220:
		tok = lex.getToken()
		if tok == 90:
			if E(v):
				tok = lex.getToken()
				if tok == 140:
					v[-1] = math.log(v[-1])
					return True
	#exp(E)
	elif tok == 260:
		tok = lex.getToken()
		if tok == 90:
			if E(v):
				tok = lex.getToken()
				if tok == 140:
					v[-1] = math.exp(v[-1])
					return True
		return False
	#num
	elif tok == 50:
		v.append(int(lex.getLexema()))
		return True
	return False

if G(v):
	print(v[0]) 
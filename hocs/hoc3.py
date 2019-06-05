import ply.yacc as yacc
from lex3 import tokens
from mathe import Pow, Log, Log10, Exp, Sqrt
from math import sin, cos, log, sqrt, tan

vari = {}

precedence = (
	('right', 'EQUALS'),
 	('left', 'PLUS', 'MINUS'),
 	('left', 'POR', 'DIVIDE'),
 	('right', 'POW'),
 	('right', 'UMINUS')
)

def p_num(p):
	'expr : NUMBER'
	p[0] = p[1]

def p_var(p):
	'expr : VAR'
	global vari
	if p[1] not in vari:
		print("Undeclare variable")
	else:
		p[0] = vari[p[1]]

def p_var_equals_exp(p):
	'expr : VAR EQUALS expr'
	vari[p[1]] = p[3]
	p[0] = ""
	
def p_funcion(p):
	'expr : FUNCION LPAR expr RPAR'
	if p[1] == 'sin':
		p[0] = sin(p[3])
	elif p[1] == 'cos':
		p[0] == cos(p[3])
	elif p[1] == 'tan':
		p[0] == tan(p[3])
	elif p[1] == 'sqrt':
		p[0] == Sqrt(p[3])
	elif p[1] == 'log10':
		p[0] = Log10(p[3])
	elif p[1] == 'exp':
		p[0] = Exp(p[3])


def p_exp_plus_exp(p):
	'expr : expr PLUS expr'
	p[0] = p[1] + p[3]

def p_exp_min_exp(p):
	'expr : expr MINUS expr'
	p[0] = p[1] - p[3]

def p_exp_por_exp(p):
	'expr : expr POR expr'
	p[0] = p[1] * p[3]

def p_exp_div_exp(p):
	'expr : expr DIVIDE expr'
	if p[3] == 0:
		print("Error. Division entre 0")
	else:
		p[0] = p[1] / p[3]

def p_par_exp_par(p):
	'expr : LPAR expr RPAR'
	p[0] = p[2]

def p_exp_pow_exp(p):
	'expr : expr POW expr'
	p[0] = Pow(p[1], p[3])

def p_min_exp(p):
	'expr : MINUS expr %prec UMINUS'
	p[0] = p[2] * (-1)

def p_error(p):
	print("Syntax Error")

parser = yacc.yacc()

while True:
    s=input();
    result = parser.parse(s)
    print(result)
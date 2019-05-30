import ply.yacc as yacc
from lex2 import tokens

precedence = (
	('right', 'EQUALS'),
 	('left', 'PLUS', 'MINUS'),
 	('left', 'POR', 'DIVIDE')
)

def p_num(p):
	'expr : NUMBER'
	p[0] = p[1]

def p_var(p):
	'expr : VAR'
	p[0] = p[1]

def p_var_equals_exp(p):
	'expr : VAR EQUALS expr'
	p[1] = p[3]
	p[0] = p[1]

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

def p_min_exp(p):
	'expr : MINUS expr'
	p[0] = p[2] * (-1)

def p_error(p):
	print("Syntax Error")

parser = yacc.yacc()

while True:
    s=input();
    result = parser.parse(s)
    print(result)
import ply.yacc as yacc
from lex import tokens

precedence = (
 	('left', 'PLUS', 'MINUS'),
 	('left', 'POR', 'DIVIDE'),
)

def p_exp_num(p):
	'expr : NUMBER'
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
	p[0] = p[1] / p[3]

def p_par_exp_par(p):
	'expr : LPAR expr RPAR'
	p[0] = p[2]

def p_error(p):
	print("Syntax Error")

#Build the parser
parser = yacc.yacc()

while True:
    s=input();
    result = parser.parse(s)
    print(result)
import ply.lex as lex

tokens = (
	'NUMBER',
	'PLUS',
	'MINUS',
	'POR',
	'DIVIDE',
	'LPAR',
	'RPAR',
	'EQUALS',
	'VAR'
)

#Regular expressions for simple tokens
t_PLUS = r'\+'
t_MINUS = r'-'
t_POR = r'\*'
t_DIVIDE = r'/'
t_LPAR = r'\('
t_RPAR = r'\)'
t_EQUALS = r'='
t_VAR = r'[a-z]'

#Regular expression for NUMBER
def t_NUMBER(t):
	r'\d+'
	t.value = int(t.value)
	return t

def t_error(t):
	print("Illegal character '%s'" % t.value[0])
	t.lexer.skip(1)	

lexer = lex.lex()
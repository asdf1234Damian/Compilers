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
	'POW',
	'VAR',
	'UMINUS',
	'FUNCION'
)

t_PLUS = r'\+'
t_MINUS = r'-'
t_POR = r'\*'
t_DIVIDE = r'/'
t_LPAR = r'\('
t_RPAR = r'\)'
t_EQUALS = r'='
t_VAR = r'[a-z]'
t_POW = r'\^'

t_ignore = r' '

def t_FUNCION(t):
	r'sin|cos|sqrt|log|log10|exp|tan'
	t.type = 'FUNCION'
	return t

def t_NUMBER(t):
	r'\d+'
	t.value = int(t.value)
	return t

def t_var(t):
	r'[a-z]+'
	t.type = 'VAR'
	return t

def t_error(t):
	print("Illegal character '%s'" % t.value[0])
	t.lexer.skip(1)	

lexer = lex.lex()
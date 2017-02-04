import ply.lex as lex

reserved_words = (
	'while',
	'print',
	'com',
	'if',
	'then',
	'else',
	'endif',
	'do',
	'endwhile'
)

tokens = (
	'NUMBER',
	'ADD_OP',
	'MUL_OP',
	'CMP_OP',
	'EQ_OP',
	'NEQ_OP',
	'VARIABLE',
	'IDENTIFIER',
	'STRING',
	'NEWLINE',
) + tuple(map(lambda s:s.upper(),reserved_words))

literals = '();={}:.#@'

def t_ADD_OP(t):
	r'[+-]'
	return t

def t_MUL_OP(t):
	r'[*/]'
	return t

def t_CMP_OP(t):
	r'[<>]'
	return t

def t_EQ_OP(t):
	r'=='
	return t

def t_NEQ_OP(t):
	r'!='
	return t

def t_NUMBER(t):
	r'\d+(\.\d+)?'
	try:
		t.value = float(t.value)
	except ValueError:
		print ("Line %d: Problem while parsing %s!" % (t.lineno,t.value))
		t.value = 0
	return t

def t_VARIABLE(t):
	r'\$[A-Za-z_]\w*'
	return t

def t_IDENTIFIER(t):
	r'[A-Za-z_]\w*'
	if t.value in reserved_words:
		t.type = t.value.upper()
	return t

def t_STRING(t):
	r'\"(.*?)\"'
	return t

def t_NEWLINE(t):
	r'\n+'
	t.lexer.lineno += len(t.value)
	return t

t_ignore  = ' \t'

def t_error(t):
	print ("Illegal character '%s'" % repr(t.value[0]))
	t.lexer.skip(1)

lex.lex()

if __name__ == "__main__":
	import sys
	prog = open(sys.argv[1]).read()

	lex.input(prog)

	while 1:
		tok = lex.token()
		if not tok: break
		print ("line %d: %s(%s)" % (tok.lineno, tok.type, tok.value))

import ply.lex as lex

# Our reserved words
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

# Our tokens
tokens = (
	'NUMBER',
	'ADD_OP',
	'MUL_OP',
	'CMP_OP',
	'EQ_OP',
	'NEQ_OP',
	'VARIABLE',
	'TAG',
	'STRING',
	'NEWLINE',
) + tuple(map(lambda s:s.upper(),reserved_words))

# Literals
# . for classes
# # for ids
# @ for content
# {} for imbrication
literals = '();={}:.#@'

# Additions
def t_ADD_OP(t):
	r'[+-]'
	return t

# Multiplications
def t_MUL_OP(t):
	r'[*/]'
	return t

# Comparisons
def t_CMP_OP(t):
	r'[<>]'
	return t

# Equalities
def t_EQ_OP(t):
	r'=='
	return t

# Inequalities
def t_NEQ_OP(t):
	r'!='
	return t

# Number
def t_NUMBER(t):
	r'\d+(\.\d+)?'
	try:
		t.value = float(t.value) # Converted in float
	except ValueError:
		print ("Line %d: Problem while parsing %s!" % (t.lineno,t.value))
		t.value = 0
	return t

# Variables
def t_VARIABLE(t):
	r'\$[A-Za-z_]\w*'
	return t

# Tag
def t_TAG(t):
	r'[A-Za-z_]\w*'
	if t.value in reserved_words: # If in reserved words, assign type
		t.type = t.value.upper()
	return t

# Strings
def t_STRING(t):
	r'\"(.*?)\"'
	return t

# Newline
def t_NEWLINE(t):
	r'\n+'
	t.lexer.lineno += len(t.value)
	return t

t_ignore  = ' \t'

# Error
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

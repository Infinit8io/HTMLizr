import ply.yacc as yacc

from lex import tokens
import AST

vars = {}

# Statement are statements
def p_programme_statement(p):
    ''' programme : statement '''
    p[0] = AST.ProgramNode(p[1])

# Recursive programme can be a statement followed by a programme
def p_programme_recursive(p):
    ''' programme : statement programme '''
    p[0] = AST.ProgramNode([p[1]]+p[2].children)


# Statements can be assignations, structures, components, identifier, expression or imbrication
def p_statement(p):
    ''' statement : assignation
        | structure
        | component
        | identifier
        | expression
        | imbrication '''
    p[0] = p[1]

# Newlines
def p_statement_newline(p):
    ''' statement : NEWLINE '''
    p[0] = AST.NewLineNode()

# Simple IF ... THEN condition creates AST.CondNode
# expression between IF and THEN, NEWLINE and programme before the ENDIF reserved word
def p_condition(p):
    ''' statement : IF expression THEN NEWLINE programme ENDIF'''
    p[0] = AST.CondNode([p[2], p[5]])

# IF ... THEN ... ELSE ... ENDIF condition creates CondNode
def p_condition_else(p):
    ''' statement : IF expression THEN NEWLINE programme ELSE NEWLINE programme ENDIF'''
    p[0] = AST.CondNode([p[2], p[5], p[8]])

# Imbrications to have tags in other tags
# Imbricated programme is between { }
def p_imbrication(p):
    ''' imbrication : identifier '{' programme '}' '''
    p[1].addChild(p[3])
    p[0] = p[1]

# A print of you want to display variables content. Creates a PrintNode
def p_statement_print(p):
    ''' statement : PRINT expression '''
    p[0] = AST.PrintNode(p[2])

# While structure with the reserved words WHILE .. DO .. ENDWHILE
def p_structure(p):
    ''' structure : WHILE expression DO NEWLINE programme ENDWHILE '''
    p[0] = AST.WhileNode([p[2],p[5]])

# Components for Bootstrap, will get the content of that comp in components/xxx.html
# The reserved word is COM:nameofcomponent
def p_component(p):
    ''' component : COM ':' TAG '''
    p[0] = AST.ComponentNode(AST.TokenNode(p[3]))

# Identifier for tags properties such as ID, classes and content value
# When three elements are specified
def p_identifier_three_element(p):
    ''' identifier : TAG elem_parts elem_parts elem_parts'''
    p[0] = AST.TagNode([AST.TagNameNode(AST.TokenNode(p[1])), p[2], p[3], p[4]])

# When two elements are specified
def p_identifier_two_element(p):
    ''' identifier : TAG elem_parts elem_parts'''
    p[0] = AST.TagNode([AST.TagNameNode(AST.TokenNode(p[1])), p[2], p[3]])

# When only one element is specified
def p_identifier_one_element(p):
    ''' identifier : TAG elem_parts '''
    p[0] = AST.TagNode([AST.TagNameNode(AST.TokenNode(p[1])), p[2]])

# Single tag identifier
def p_identifier(p):
    ''' identifier : TAG '''
    p[0] = AST.TagNode(AST.TagNameNode(AST.TokenNode(p[1])))

# Argument for the value in the class, id, value for a tag.
def p_arguments(p):
    ''' argument : STRING
            | VARIABLE
            | NUMBER '''
    p[0] = p[1].replace("\"", "")

# Elements parts for a tag. Can be a class, ID or content
# Used in the previous p_identifier for tags
def p_elements_identifier(p):
    '''elem_parts : class
        | id
        | content '''
    p[0] = p[1]

# Tag class definition. Part of the elem_parts identifier
def p_class(p):
    '''class : '.' argument '''
    p[0] = AST.ClassNode(AST.TokenNode(p[2]))

# Tag ID definition. Part of the elem_parts identifier
def p_id(p):
    '''id : '#' argument '''
    p[0] = AST.IdNode(AST.TokenNode(p[2]))

# Tag content definition. Part of the elem_parts identifier
def p_content(p):
    '''content : '@' argument '''
    p[0] = AST.ContentNode(AST.TokenNode(p[2]))

# Mathematical expression for multiplication in the xxx * 2 way
def p_identifier_mulop_expression(p):
    '''expression : identifier MUL_OP expression
            | component MUL_OP expression'''
    p[0] = AST.OpTagNode(p[2], [p[1], p[3]])

# Mathematical expression for multiplication in the 2 * xxx way
def p_expression_mulop_identifier(p):
    '''expression : expression MUL_OP identifier
            | expression MUL_OP component'''
    p[0] = AST.OpTagNode(p[2], [p[3], p[1]])

# Mathematical expression for imbrication multiplication
def p_expression_imbrication(p):
    '''imbrication : expression MUL_OP imbrication '''
    p[0] = AST.OpTagNode(p[2], [p[3], p[1]])

def p_imbrication_expression(p):
    '''imbrication : imbrication MUL_OP expression '''
    p[0] = AST.OpTagNode(p[2], [p[1], p[3]])

# Mathematical expressions
def p_expression_op(p):
    '''expression : expression ADD_OP expression
            | expression MUL_OP expression
            | expression CMP_OP expression
            | expression EQ_OP expression
            | expression NEQ_OP expression'''
    p[0] = AST.OpNode(p[2], [p[1], p[3]])

# Number or variable
def p_expression_num_or_var(p):
    '''expression : NUMBER
        | VARIABLE '''
    p[0] = AST.TokenNode(p[1])

# String expression
def p_expression_string(p):
    '''expression : STRING '''
    p[0] = AST.TokenNode(p[1].replace("\"", ""))

# Brackets expression
def p_expression_paren(p):
    '''expression : '(' expression ')' '''
    p[0] = p[2]

# Minus
def p_minus(p):
    ''' expression : ADD_OP expression %prec UMINUS'''
    p[0] = AST.OpNode(p[1], [p[2]])

# Assignation
def p_assign(p):
    ''' assignation : VARIABLE '=' expression '''
    p[0] = AST.AssignNode([AST.TokenNode(p[1]),p[3]])

# For errors management
def p_error(p):
    if p:
        print ("Syntax error in line %d" % p.lineno)
        yacc.errok()
    else:
        print ("Syntax error: unexpected end of file!")

# Precedence
precedence = (
    ('left', 'ADD_OP'),
    ('left', 'MUL_OP'),
    ('right', 'UMINUS'),
)

def parse(program):
    return yacc.parse(program)

yacc.yacc(outputdir='generated')

if __name__ == "__main__":
    import sys

    prog = open(sys.argv[1]).read()
    result = yacc.parse(prog)
    if result:
        print (result)

        import os
        graph = result.makegraphicaltree()
        name = os.path.splitext(sys.argv[1])[0]+'-ast.pdf'
        graph.write_pdf(name)
        #print ("wrote ast to", name)
    else:
        print ("Parsing returned no result!")

import ply.yacc as yacc

from lex5 import tokens
import AST

vars = {}

def p_programme_statement(p):
    ''' programme : statement '''
    p[0] = AST.ProgramNode(p[1])

def p_programme_recursive(p):
    ''' programme : statement programme '''
    p[0] = AST.ProgramNode([p[1]]+p[2].children)

def p_programme_fin(p):
    ''' programme : statement ';' '''
    p[0] = AST.ProgramNode(p[1])

def p_statement(p):
    ''' statement : assignation
        | structure
        | component
        | identifier
        | expression
        | chevron '''
    p[0] = p[1]

def p_statement_newline(p):
    ''' statement : NEWLINE '''
    p[0] = AST.NewLineNode()

def p_condition(p):
    ''' statement : IF expression THEN NEWLINE programme ENDIF'''
    p[0] = AST.CondNode([p[2], p[5]])

def p_condition_else(p):
    ''' statement : IF expression THEN NEWLINE programme ELSE NEWLINE programme ENDIF'''
    p[0] = AST.CondNode([p[2], p[5], p[8]])

def p_chevron(p):
    ''' chevron : identifier '{' programme '}' '''
    p[0] = AST.SonNode([p[1], p[3]])

def p_statement_print(p):
    ''' statement : PRINT expression '''
    p[0] = AST.PrintNode(p[2])

def p_structure(p):
    ''' structure : WHILE expression DO NEWLINE programme ENDWHILE '''
    p[0] = AST.WhileNode([p[2],p[5]])

def p_component(p):
    ''' component : COM ':' IDENTIFIER '''
    p[0] = AST.ComponentNode(AST.TokenNode(p[3]))

def p_identifier_no_args(p):
    ''' identifier : IDENTIFIER '''
    p[0] = AST.TagNode([p[1], None, None, None])

def p_identifier_id(p):
    ''' identifier : IDENTIFIER '#' STRING '''
    p[0] = AST.TagNode([p[1], p[3], None, None])

def p_identifier_class(p):
    ''' identifier : IDENTIFIER '.' STRING '''
    p[0] = AST.TagNode([p[1], None, p[3], None])

def p_identifier_value(p):
    ''' identifier : IDENTIFIER '@' STRING '''
    p[0] = AST.TagNode([p[1], None, None, p[3]])

def p_identifier_id_class(p):
    ''' identifier : IDENTIFIER '#' STRING '.' STRING '''
    p[0] = AST.TagNode([p[1], p[3], p[5], None])

def p_identifier_class_id(p):
    ''' identifier : IDENTIFIER '.' STRING '#' STRING '''
    p[0] = AST.TagNode([p[1], p[5], p[3], None])

def p_identifier_id_value(p):
    ''' identifier : IDENTIFIER '#' STRING '@' STRING '''
    p[0] = AST.TagNode([p[1], p[3], None, p[5]])

def p_identifier_value_id(p):
    ''' identifier : IDENTIFIER '@' STRING '#' STRING '''
    p[0] = AST.TagNode([p[1], p[5], None, p[3]])

def p_identifier_class_value(p):
    ''' identifier : IDENTIFIER '.' STRING '@' STRING '''
    p[0] = AST.TagNode([p[1], None, p[3], p[5]])

def p_identifier_value_class(p):
    ''' identifier : IDENTIFIER '@' STRING '.' STRING '''
    p[0] = AST.TagNode([p[1], None, p[5], p[3]])

def p_identifier_id_class_value(p):
    ''' identifier : IDENTIFIER '#' STRING '.' STRING '@' STRING '''
    p[0] = AST.TagNode([p[1], p[3], p[5], p[7]])

def p_identifier_id_value_class(p):
    ''' identifier : IDENTIFIER '#' STRING '@' STRING '.' STRING '''
    p[0] = AST.TagNode([p[1], p[3], p[7], p[5]])

def p_identifier_class_id_value(p):
    ''' identifier : IDENTIFIER '.' STRING '#' STRING '@' STRING '''
    p[0] = AST.TagNode([p[1], p[5], p[3], p[7]])

def p_identifier_class_value_id(p):
    ''' identifier : IDENTIFIER '.' STRING '@' STRING '#' STRING '''
    p[0] = AST.TagNode([p[1], p[7], p[3], p[5]])

def p_identifier_value_id_class(p):
    ''' identifier : IDENTIFIER '@' STRING '#' STRING '.' STRING '''
    p[0] = AST.TagNode([p[1], p[5], p[7], p[3]])

def p_identifier_value_class_id(p):
    ''' identifier : IDENTIFIER '@' STRING '.' STRING '#' STRING '''
    p[0] = AST.TagNode([p[1], p[7], p[5], p[2]])

def p_identifier_mulop_expression(p):
    '''expression : identifier MUL_OP expression '''
    p[0] = AST.OpTagNode(p[2], [p[1], p[3]])

def p_expression_mulop_identifier(p):
    '''expression : expression MUL_OP identifier '''
    p[0] = AST.OpTagNode(p[2], [p[3], p[1]])

def p_expression_op(p):
    '''expression : expression ADD_OP expression
            | expression MUL_OP expression
            | expression CMP_OP expression
            | expression EQ_OP expression
            | expression NEQ_OP expression'''
    p[0] = AST.OpNode(p[2], [p[1], p[3]])

def p_expression_num_or_var(p):
    '''expression : NUMBER
        | VARIABLE '''
    p[0] = AST.TokenNode(p[1])

def p_expression_string(p):
    '''expression : STRING '''
    p[0] = AST.TokenNode(p[1])

def p_expression_chevron(p):
    '''expression : chevron'''
    p[0] = AST.SonNode(p[1])

def p_expression_paren(p):
    '''expression : '(' expression ')' '''
    p[0] = p[2]

def p_minus(p):
    ''' expression : ADD_OP expression %prec UMINUS'''
    p[0] = AST.OpNode(p[1], [p[2]])

def p_assign(p):
    ''' assignation : VARIABLE '=' expression '''
    p[0] = AST.AssignNode([AST.TokenNode(p[1]),p[3]])

def p_error(p):
    if p:
        print ("Syntax error in line %d" % p.lineno)
        yacc.errok()
    else:
        print ("Syntax error: unexpected end of file!")

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
        #graph.write_pdf(name)
        #print ("wrote ast to", name)
    else:
        print ("Parsing returned no result!")

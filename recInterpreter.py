import AST
from AST import addToClass
from functools import reduce
import itertools


operations = {
    '+' : lambda x, y: x+y,
    '-' : lambda x, y: x-y,
    '*' : lambda x, y: x*y,
    '/' : lambda x, y: x/y,
    '<' : lambda x, y: x<y,
    '>' : lambda x, y: x>y,
    '==' : lambda x,y: x == y,
    '!=' : lambda x,y: x != y
}

vars = {}
vars["result"] = ""

@addToClass(AST.ProgramNode)
def execute(self):
    for c in self.children:
        c.execute()

@addToClass(AST.NewLineNode)
def execute(self):
    pass

@addToClass(AST.TokenNode)
def execute(self):
    if isinstance(self.tok, str):
        try:
            return vars[self.tok]
        except KeyError:
            pass
    if not isinstance(self.tok, AST.TokenNode):
        return self.tok
    else:
        return self.tok.execute()

@addToClass(AST.OpNode)
def execute(self):
    args = [c.execute() for c in self.children]
    if len(args) == 1:
        args.insert(0, 0)
    if(isinstance(args[0], str)):
        for i in range(1, len(args)):
            args[i] = str(args[i])
    return reduce(operations[self.op], args)

@addToClass(AST.OpTagNode)
def execute(self):
    for i in range(int(self.children[1].tok)):
        self.children[0].execute()

@addToClass(AST.AssignNode)
def execute(self):
    vars[self.children[0].tok] = self.children[1].execute()

@addToClass(AST.WhileNode)
def execute(self):
    while self.children[0].execute() != 0: # Tant qu'il y a des noeuds
        self.children[1].execute() # On exécute

@addToClass(AST.PrintNode)
def execute(self):
    vars["result"] += str(self.children[0].execute()).replace("\"", "")

@addToClass(AST.ComponentNode)
def execute(self):
    for c in self.children:
        with open("./components/" + c.tok + ".html") as file:
            data = file.read()
            vars["result"] += data

@addToClass(AST.TagNode)
def execute(self):
    if self is not None:
        str = ""
        tagname = None
        value = None
        program = None
        for c in self.children:
            if isinstance(c, AST.TagNameNode):
                tagname = c.execute()
                str += "<"+tagname
            if isinstance(c, AST.IdNode) or isinstance(c, AST.ClassNode):
                str += c.execute()
            if isinstance(c, AST.ContentNode):
                value = c.execute()
            if isinstance(c, AST.ProgramNode):
                program = c
        str += ">"
        if value is not None:
            str += value.replace("\"", "")
        vars["result"] += str;
        str = ""
        if program is not None:
            result = program.execute()
            if result is not None:
                str += result
        str += "</"+tagname+">"
        vars["result"] += str;

@addToClass(AST.TagNameNode)
def execute(self):
    return self.children[0].execute()


@addToClass(AST.IdNode)
def execute(self):
    return " id=\""+str(self.children[0].execute()).replace("\"", "")+"\""

@addToClass(AST.ClassNode)
def execute(self):
    return " class=\""+str(self.children[0].execute()).replace("\"", "")+"\""

@addToClass(AST.ContentNode)
def execute(self):
    return str(self.children[0].execute())

@addToClass(AST.CondNode)
def execute(self):
    cond_result = self.children[0].execute()
    if len(self.children) == 2:
        if cond_result != 0:
            self.children[1].execute()
    else:
        if cond_result != 0:
            self.children[1].execute()
        else:
            self.children[2].execute()

if __name__ == '__main__':
    from parserHTMLizr import parse
    import sys
    print("Started Program")
    result = ""
    prog = open(sys.argv[1]).read()
    ast = parse(prog)
    ast.execute()
    print(vars["result"])

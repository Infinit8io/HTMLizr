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

@addToClass(AST.PrintNode)
def execute(self):
    vars["result"] += self.children[0].execute()
    print(self.children[0].execute())

@addToClass(AST.WhileNode)
def execute(self):
    while self.children[0].execute() != 0: # Tant qu'il y a des noeuds
        self.children[1].execute() # On exécute


@addToClass(AST.ComponentNode)
def execute(self):
    for c in self.children:
        with open("./components/" + c.tok + ".html") as file:
            data = file.read()
            vars["result"] += data
            print(data)

@addToClass(AST.TagNode)
def execute(self):
    if self is not None:
        tagline = ""
        tagline += "<" + self.name # Open tag
        if self.id is not None: # id if needed
            tagline += ' id=' + self.id + ''
        if self.classe is not None: # class if needed
            tagline += ' class=' + self.classe + ''
        tagline += ">" # Open tag end
        if self.value is not None:
            tagline += (self.value).replace("\"", "")
        vars["result"] += tagline;
        print(tagline)
        for c in self.children:
            c.execute()
        tagline = "</" + self.tok[0] + ">\n" # End tag
        vars["result"] += tagline;
        print(tagline)

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
    from parser5 import parse
    import sys
    print("Started Program")
    result = ""
    prog = open(sys.argv[1]).read()
    ast = parse(prog)
    ast.execute()

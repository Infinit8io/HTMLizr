import AST
from AST import addToClass
from functools import reduce


operations = {
    '+' : lambda x, y: x+y,
    '-' : lambda x, y: x-y,
    '*' : lambda x, y: x*y,
    '/' : lambda x, y: x/y
}

vars = {}

@addToClass(AST.ProgramNode)
def execute(self):
    for c in self.children:
        c.execute()

@addToClass(AST.TokenNode)
def execute(self):
    if isinstance(self.tok, str):
        try:
            return vars[self.tok]
        except KeyError:
            print("*** Error : variable %s undefined !" % self.tok)
    return self.tok

@addToClass(AST.OpNode)
def execute(self):
    args = [c.execute() for c in self.children]
    if len(args) == 1:
        args.insert(0,0)
    #return reduce(operations[self.op], args)
    return 42

@addToClass(AST.AssignNode)
def execute(self):
    vars[self.children[0].tok] = self.children[1].execute()

@addToClass(AST.PrintNode)
def execute(self):
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
            print(data)

@addToClass(AST.SonNode)
def execute(self):
    print("Execute SonNode")
    for c in self.children:
        print("ok")
        print(c.tok)


@addToClass(AST.TagNode)
def execute(self):
    print("Execute TagNode")
    tagline = ""
    tagline += "<" + self.name # Open tag
    if self.id is not None: # id if needed
        tagline += ' id="' + self.id + '"'
    if self.classe is not None: # class if needed
        tagline += ' class="' + self.classe + '"'
    tagline += ">" # Open tag end

    # Inside that div here

    tagline += "<" + self.tok[0] + ">" # End tag
    print(tagline)



if __name__ == '__main__':
    from parser5 import parse
    import sys
    print("Started Program")
    prog = open(sys.argv[1]).read()
    ast = parse(prog)
    ast.execute()

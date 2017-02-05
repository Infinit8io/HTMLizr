import AST
from AST import addToClass
from functools import reduce
import itertools

# Operations
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
# we will stock the final result here in vars["result"]
vars["result"] = ""

# Manage the ProgramNode. Execute all child.
@addToClass(AST.ProgramNode)
def execute(self):
    for c in self.children:
        c.execute()

# Manage the NewLineNode. Add a carriage return
@addToClass(AST.NewLineNode)
def execute(self):
    vars["result"] += "\n"

# Manage the TokenNode. Return value of token
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

# Manage the OpNode. It will do the mathematical operations.
@addToClass(AST.OpNode)
def execute(self):
    args = [c.execute() for c in self.children]
    if len(args) == 1:
        args.insert(0, 0)
    if(isinstance(args[0], str)):
        for i in range(1, len(args)):
            args[i] = str(args[i])
    return reduce(operations[self.op], args)

# Manage the OpTagNode. Will execute the first child x times.
@addToClass(AST.OpTagNode)
def execute(self):
    for i in range(int(self.children[1].tok)):
        self.children[0].execute()

# Manage the AssignNode. It will store the variables in vars
@addToClass(AST.AssignNode)
def execute(self):
    vars[self.children[0].tok] = self.children[1].execute()

# Manage the WhileNode. It will do the while loop.
@addToClass(AST.WhileNode)
def execute(self):
    while self.children[0].execute() != 0: # Tant qu'il y a des noeuds
        self.children[1].execute() # On exécute

# Manage the PrintNode. It will add to the result the value we want to print.
@addToClass(AST.PrintNode)
def execute(self):
    vars["result"] += str(self.children[0].execute()).replace("\"", "")

# Manage the ComponentNode. It will add the component from a file.
@addToClass(AST.ComponentNode)
def execute(self):
    for c in self.children:
        with open("./components/" + c.tok + ".html") as file:
            data = file.read()
            vars["result"] += data

# Manage the TagNode. It will add the html tag with its caracteristics.
@addToClass(AST.TagNode)
def execute(self):
    if self is not None:
        str = ""
        tagname = None
        value = None
        program = None
        # Begin of the html tag
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
        # add the value between the tag
        if value is not None:
            str += value.replace("\"", "")
        vars["result"] += str;
        str = ""
        # Imbrication of the program in the html tag
        if program is not None:
            result = program.execute()
            if result is not None:
                str += result
        # End of the html tag
        str += "</"+tagname+">"
        vars["result"] += str;

# Manage the TagNameNode. Return the value of the name tag.
@addToClass(AST.TagNameNode)
def execute(self):
    return self.children[0].execute()

# Manage the IdNode. Return the id caracterstic for a tag. id="value"
@addToClass(AST.IdNode)
def execute(self):
    return " id=\""+str(self.children[0].execute()).replace("\"", "")+"\""

# Manage the ClassNode. Return the class caracterstic for a tag. class="value"
@addToClass(AST.ClassNode)
def execute(self):
    return " class=\""+str(self.children[0].execute()).replace("\"", "")+"\""

# Manage the ContentNode. Return the value
@addToClass(AST.ContentNode)
def execute(self):
    return str(self.children[0].execute())

# Manage the CondNode. It will test the condition and execute the good child.
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
    prog = open(sys.argv[1]).read()
    ast = parse(prog)
    ast.execute()
    # Display in the console the final result.
    print(vars["result"])

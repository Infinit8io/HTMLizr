from optparse import OptionParser
import webbrowser
import os
from recInterpreter import *


if __name__ == '__main__':
    from parser5 import parse
    import sys

    parser = OptionParser()
    parser.add_option("-f", "--inputfile", dest="input_filename", help="Source filename", default="examples/demo1.htmlzr", metavar="INFILE")
    parser.add_option("-o", "--outputfile", dest="output_filename", help="Destination filename", default="pages/htmlizr.html", metavar="OUTFILE")
    parser.add_option("-p", "--page", dest="page_mode", help="Fullpage creation mode", default=True, metavar="COMPMODE")
    parser.add_option("-c", "--comp", dest="comp_mode", help="Composant creation mode", metavar="COMPMODE")

    (options, args) = parser.parse_args()

    # Open file to read
    prog = open(options.input_filename).read()
    ast = parse(prog)
    ast.execute()

    # Get the generated HTML
    generatedHTML = vars["result"]

    # When creating a new component
    if options.comp_mode is not None:
        print("Creating a new component")
        f = open("components/" + options.comp_mode, 'w')
    else:
        # Open file to write in
        f = open("pages/" + options.output_filename, 'w')

    # Si on doit créer une page complète utilisable
    if options.page_mode:
        header = open("components/header.html").read()
        footer = open("components/footer.html").read()
        f.write(header + generatedHTML + footer)
        webbrowser.open(os.path.abspath("pages/" + options.output_filename), new=2)
        f.close()
    else:
        f.write(generatedHTML)
        f.close()
      # you can omit in most cases as the destructor will call it

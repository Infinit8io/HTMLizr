from optparse import OptionParser
import webbrowser
import os
from recInterpreter import *


if __name__ == '__main__':
    from parserHTMLizr import parse
    import sys

    # Manage the args
    parser = OptionParser()
    parser.add_option("-f", "--inputfile", dest="input_filename", help="HTMLizr source file from which we will generate the HTML code", default="examples/demo1.htmlzr", metavar="INFILE")
    parser.add_option("-o", "--outputfile", dest="output_filename", help="The destination page filename", default="htmlizr.html", metavar="OUTFILE")
    parser.add_option("-p", "--page", dest="page_mode", help="Fullpage creation mode", default=True, metavar="PAGEMODE")
    parser.add_option("-c", "--comp", dest="comp_mode", help="Composant creation mode", metavar="COMPMODE")

    (options, args) = parser.parse_args()

    # Open file to read
    prog = open(options.input_filename).read()
    ast = parse(prog) # Parse the code
    ast.execute() # Execution

    # Get the generated HTML
    generatedHTML = vars["result"]

    # When creating a new component
    if options.comp_mode is not None:
        print("Creating a new component")
        f = open("components/" + options.comp_mode, 'w')
    else:
        # Open file to write in
        f = open("pages/" + options.output_filename, 'w')

    # If we have to create a fullpage with html headers
    if options.page_mode:
        header = open("components/header.html").read() # Get the HTML header page
        footer = open("components/footer.html").read() # Get the HTML footer page
        f.write(header + generatedHTML + footer) # Sandwich of content between header and footer
        webbrowser.open(os.path.abspath("pages/" + options.output_filename), new=2) # Open the browser with the result
        f.close()
    # If it's a simple component
    else:
        f.write(generatedHTML)
        f.close()

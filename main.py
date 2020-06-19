import logging
logging.basicConfig(level = logging.INFO)

from code_parser import parse_code
from graphviz import Digraph

def main():
    file_name = "sample_code.py"
    file_object = open(file_name, 'r')
    logging.info("The file %s was opened and successfully read.", file_name)

    file_contents = []

    while True:
        file_line = file_object.readline()
        if not file_line:
            break
        # Removing any blank lines in the source code
        if len(file_line.strip()) != 0:
            file_contents.append(file_line.rstrip())
    parse_code(file_contents)

main()

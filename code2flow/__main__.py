import code2flow
from code2flow import flowchart_generator

import sys

def main():
    arguments = [argument for argument in sys.argv[1:] if not argument.startswith("-")]
    #options = [option for option in sys.argv[1:] if option.startswith("-")]

    if(len(arguments) == 0):
        print("A python module / CLI command to create flow charts from python code.")
        print("")
        print("Usage: code2flow <file name>")
        print("")
    else:
        file_name = arguments[0]

        function_dot_codes = flowchart_generator.read_source_code(file_name)

        for function_name in function_dot_codes:
            print(function_name)
            print(function_dot_codes[function_name])
            print("")

if __name__ == "__main__":
    main()

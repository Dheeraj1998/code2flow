import logging
import re

FUNCTION_DEFINITION = 'function_definition'
IF_CONDITION = 'if_condition'
ELIF_CONDITION = 'elif_condition'
ELSE_CONDITION = 'else_condition'
ASSIGNMENT_CODE = 'assignment_code'
GENERTIC_CODE = 'generic_code'

logging.basicConfig(level = logging.INFO)
code_content = ['def main():', '    print("Hello world!")', '    variableValue = 10', '    if(variableValue < 5):', '        print("variableValue is less than 5.")', '    else:', '        print("variableValue is greater than 5.")', 'main()']

def check_indentation(code_line):
    return len(code_line) - len(code_line.lstrip())

def determine_line_type(code_line):
    code_line = code_line.strip()

    if code_line.startswith('def'):
        return(FUNCTION_DEFINITION)
    elif code_line.startswith('if'):
        return(IF_CONDITION)
    elif code_line.startswith('elif'):
        return(ELIF_CONDITION)
    elif code_line.startswith('else'):
        return(ELSE_CONDITION)
    elif re.findall("[\w]*=.*", code_line):
        return(ASSIGNMENT_CODE)
    else:
        return(GENERTIC_CODE)

def parse_code(code_content):
    global_code_flow = []
    function_codes = {}
    current_function_stack = []
    indentation_level_stack = []

    for code_line in code_content:
        line_type = determine_line_type(code_line)
        indentation_level = check_indentation(code_line)
        stripped_code_line = code_line.strip()
        print(code_line, line_type, indentation_level)
        if (determine_line_type == FUNCTION_DEFINITION):
            indentation_level_stack.append(indentation_level)
            current_function_stack.append(code_line)
            function_codes[code_line] = []
        else:
            if len(indentation_level_stack) == 0:
                global_code_flow.append(stripped_code_line)
            elif indentation_level > current_function_stack[len(current_function_stack) - 1]:
                function_codes[current_function_stack[len(current_function_stack) - 1]].append(code_line)

    print(function_codes)

parse_code(code_content)

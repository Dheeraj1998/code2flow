import re

FUNCTION_DEFINITION = 'function_definition'
IF_CONDITION = 'if_condition'
ELIF_CONDITION = 'elif_condition'
ELSE_CONDITION = 'else_condition'
ASSIGNMENT_CODE = 'assignment_code'
GENERTIC_CODE = 'generic_code'

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

        # Creating an empty array code block corresponding to the function name
        if (line_type == FUNCTION_DEFINITION):
            indentation_level_stack.append(indentation_level)
            current_function_stack.append(stripped_code_line)
            function_codes[code_line] = []
        else:
            # Adding to the global code flow when there is no indentation in the code
            if len(indentation_level_stack) == 0:
                global_code_flow.append(stripped_code_line)
            # Adding to the specific code flow the indentation is greater than the top of stack
            elif indentation_level > indentation_level_stack[len(indentation_level_stack) - 1]:
                function_codes[current_function_stack[len(current_function_stack) - 1]].append([{"code_type": line_type, "indentation_level": indentation_level, "code_line": stripped_code_line}])
            # Removing the top elements of the stacks and adding the code to the global code flow
            else:
                indentation_level_stack.pop()
                current_function_stack.pop()
                global_code_flow.append(stripped_code_line)

    return global_code_flow, function_codes

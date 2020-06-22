from code_parser import IF_CONDITION, ELIF_CONDITION, ELSE_CONDITION

from graphviz import Digraph
from string import digits

import re
import uuid

IF_CONDITION_NODE_LABEL = 'Conditional node'

function_codes = {'def main():': [[{'code_type': 'generic_code', 'indentation_level': 4, 'code_line': 'print("Hello world!")'}], [{'code_type': 'assignment_code', 'indentation_level': 4, 'code_line': 'variableValue = 10'}], [{'code_type': 'if_condition', 'indentation_level': 4, 'code_line': 'if(variableValue < 5):'}], [{'code_type': 'generic_code', 'indentation_level': 8, 'code_line': 'print("Level 1.0 of loop.")'}], [{'code_type': 'if_condition', 'indentation_level': 8, 'code_line': 'if(variableValue > 10):'}], [{'code_type': 'generic_code', 'indentation_level': 12, 'code_line': 'print("Level 1.0-1 of loop.")'}], [{'code_type': 'generic_code', 'indentation_level': 12, 'code_line': 'print("Level 1.0-2 of loop.")'}], [{'code_type': 'generic_code', 'indentation_level': 12, 'code_line': 'print("Level 1.0-3 of loop.")'}], [{'code_type': 'generic_code', 'indentation_level': 8, 'code_line': 'print("Level 1.1 of loop.")'}], [{'code_type': 'generic_code', 'indentation_level': 8, 'code_line': 'print("Level 1.2 of loop.")'}], [{'code_type': 'elif_condition', 'indentation_level': 4, 'code_line': 'elif(variableValue < 10):'}], [{'code_type': 'generic_code', 'indentation_level': 8, 'code_line': 'print("Level 2.0 of loop.")'}], [{'code_type': 'else_condition', 'indentation_level': 4, 'code_line': 'else:'}], [{'code_type': 'generic_code', 'indentation_level': 8, 'code_line': 'print("Level 3.0 of loop.")'}], [{'code_type': 'generic_code', 'indentation_level': 8, 'code_line': 'print("Level 3.1 of loop.")'}], [{'code_type': 'generic_code', 'indentation_level': 8, 'code_line': 'print("Level 3.2 of loop.")'}], [{'code_type': 'generic_code', 'indentation_level': 4, 'code_line': 'print("Goodbye.")'}]]}

def create_uuid_values(required_number):
    regex_pattern = '[-0-9]'
    used_uuid_values = []

    for value in range(required_number):
        while True:
            uuid_value = str(uuid.uuid4())
            stripped_uuid_value = re.sub(regex_pattern, '', str(uuid_value))
            if stripped_uuid_value not in used_uuid_values:
                used_uuid_values.append(stripped_uuid_value)
                break
    return used_uuid_values

def generate(function_codes):
    for function_name in function_codes:
        function_content = function_codes[function_name]
        generated_uuid_values = create_uuid_values(len(function_content))
        function_dot_code = Digraph()

        used_uuid_count = 0
        code_line_stack = []
        indentation_level_stack = []
        # This stack stores the UUID required for the alternate connection to a node from a branching node
        branching_node_uuid_stack = []
        # This stack stores all the ending nodes so that they could be connected to the un-intended nodes (outer code)
        ending_node_uuid_stack = []
        previous_code_line = ''
        previous_code_type = ''
        previous_indentation_level = 0

        for code_block in function_content:
            code_block_dictionary = code_block[0]

            current_code_type = code_block_dictionary['code_type']
            current_indentation_level = code_block_dictionary['indentation_level']
            current_code_line = code_block_dictionary['code_line']

             # Adding the last code lines of each intended block
            if current_indentation_level < previous_indentation_level:
                ending_node_uuid_stack.append(previous_block_uuid)

            # Handling the cases where the flow would need to branch out (initial branch)
            if (current_code_type in [IF_CONDITION]):
                function_dot_code.node(generated_uuid_values[used_uuid_count], IF_CONDITION_NODE_LABEL)

                indentation_level_stack.append(current_indentation_level)
                code_line_stack.append(current_code_line)
                branching_node_uuid_stack.append(generated_uuid_values[used_uuid_count])
                # This node needs to be appened in cases where there isn't a terminating condition
                ending_node_uuid_stack.append(generated_uuid_values[used_uuid_count])

                # Handling the first node of the flow
                if used_uuid_count != 0:
                    function_dot_code.edge(previous_block_uuid, generated_uuid_values[used_uuid_count])
                previous_block_uuid = generated_uuid_values[used_uuid_count]
                used_uuid_count += 1
            # Handling the cases where the flow would need to branch out (after the initial branch)
            elif (current_code_type in [ELIF_CONDITION, ELSE_CONDITION]):
                code_line_stack.append(current_code_line)
            else:
                function_dot_code.node(generated_uuid_values[used_uuid_count], current_code_line)

                # Handling all nodes except the first one of the flow
                if used_uuid_count != 0:
                    # Handling the first edge after a special code line (start of indentation)
                    if len(code_line_stack) != 0:
                        function_dot_code.edge(branching_node_uuid_stack[len(branching_node_uuid_stack) - 1], generated_uuid_values[used_uuid_count], label = code_line_stack.pop(), style = 'dashed')
                        # if previous_code_type == ELSE_CONDITION:
                            # print(current_code_line)
                    else:
                        # Handling the first code line after code block (for alternate branching)
                        if current_indentation_level < previous_indentation_level:
                            # Removing the previous branching node as the code block is complete
                            branching_node_uuid_stack.pop()
                            print(current_code_line, ending_node_uuid_stack)
                            total_required_edges = len(ending_node_uuid_stack)
                            for interation in range(total_required_edges):
                                function_dot_code.edge(ending_node_uuid_stack.pop(), generated_uuid_values[used_uuid_count], style = 'dashed')
                        else:
                            function_dot_code.edge(previous_block_uuid, generated_uuid_values[used_uuid_count])
                previous_block_uuid = generated_uuid_values[used_uuid_count]
                used_uuid_count += 1

            previous_code_line = current_code_line
            previous_indentation_level = current_indentation_level
            previous_code_type = current_code_type
        print(function_dot_code)
generate(function_codes)

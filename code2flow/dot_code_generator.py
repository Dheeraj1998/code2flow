from .code_parser import IF_CONDITION, ELIF_CONDITION, ELSE_CONDITION

from graphviz import Digraph
from string import digits

import re
import uuid

STARTING_CONDITIONAL_STATEMENTS = [IF_CONDITION]
INTERMEDIATE_CONDITIONAL_STATEMENTS = [ELIF_CONDITION]
TERMINATING_CONDITIONAL_STATEMENTS = [ELSE_CONDITION]

IF_CONDITION_NODE_LABEL = 'Conditional node'

def create_node_edge(used_uuid_count, code_line_stack, function_dot_code, branching_node_uuid_stack, generated_uuid_values, current_indentation_level, previous_indentation_level, ending_node_uuid_stack, previous_block_uuid):
    # Handling all nodes except the first one of the flow
    if used_uuid_count != 0:
        # Handling the first edge after a special code line (start of indentation)
        if len(code_line_stack) != 0:
            function_dot_code.edge(branching_node_uuid_stack[len(branching_node_uuid_stack) - 1], generated_uuid_values[used_uuid_count], label = code_line_stack.pop(), style = 'dashed')
        else:
            # Handling the first code line after code block (for alternate branching)
            if current_indentation_level < previous_indentation_level:
                # Removing the previous branching node as the code block is complete
                branching_node_uuid_stack.pop()
                total_required_edges = len(ending_node_uuid_stack[len(ending_node_uuid_stack) - 1])

                for iteration in range(total_required_edges):
                    function_dot_code.edge(ending_node_uuid_stack[len(ending_node_uuid_stack) - 1].pop(), generated_uuid_values[used_uuid_count], style = 'dashed')
                # Deleting the innermost empty array of code block
                del ending_node_uuid_stack[len(ending_node_uuid_stack) - 1]
            else:
                function_dot_code.edge(previous_block_uuid, generated_uuid_values[used_uuid_count])

    return function_dot_code, code_line_stack, branching_node_uuid_stack, ending_node_uuid_stack, used_uuid_count

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
    function_dot_codes = {}

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
        previous_block_uuid = ''

        for code_block in function_content:
            code_block_dictionary = code_block[0]

            current_code_type = code_block_dictionary['code_type']
            current_indentation_level = code_block_dictionary['indentation_level']
            current_code_line = code_block_dictionary['code_line']

             # Adding the last code lines of each intended block
            if current_indentation_level < previous_indentation_level:
                ending_node_uuid_stack[len(ending_node_uuid_stack) - 1].append(previous_block_uuid)

            # Handling the cases where the flow would need to branch out (initial branch)
            if (current_code_type in STARTING_CONDITIONAL_STATEMENTS):
                function_dot_code.node(generated_uuid_values[used_uuid_count], IF_CONDITION_NODE_LABEL, shape = "diamond")
                function_dot_code, code_line_stack, branching_node_uuid_stack, ending_node_uuid_stack, used_uuid_count = create_node_edge(used_uuid_count, code_line_stack, function_dot_code, branching_node_uuid_stack, generated_uuid_values, current_indentation_level, previous_indentation_level, ending_node_uuid_stack, previous_block_uuid)

                indentation_level_stack.append(current_indentation_level)
                code_line_stack.append(current_code_line)
                branching_node_uuid_stack.append(generated_uuid_values[used_uuid_count])
                # This node needs to be appened in cases where there isn't a terminating condition
                ending_node_uuid_stack.append([generated_uuid_values[used_uuid_count]])

                previous_block_uuid = generated_uuid_values[used_uuid_count]
                used_uuid_count += 1

            # Handling the cases where the flow would need to branch out (after the initial branch)
            elif (current_code_type in INTERMEDIATE_CONDITIONAL_STATEMENTS):
                code_line_stack.append(current_code_line)
            # Handling the cases where the flow would be ending (terminating branch)
            elif (current_code_type in TERMINATING_CONDITIONAL_STATEMENTS):
                code_line_stack.append(current_code_line)
                # Removing the initial conditional block from all ending connections
                ending_node_uuid_stack[len(ending_node_uuid_stack) - 1].remove(branching_node_uuid_stack[len(branching_node_uuid_stack) - 1])
            else:
                function_dot_code.node(generated_uuid_values[used_uuid_count], current_code_line, shape = "rect")
                function_dot_code, code_line_stack, branching_node_uuid_stack, ending_node_uuid_stack, used_uuid_count = create_node_edge(used_uuid_count, code_line_stack, function_dot_code, branching_node_uuid_stack, generated_uuid_values, current_indentation_level, previous_indentation_level, ending_node_uuid_stack, previous_block_uuid)

                previous_block_uuid = generated_uuid_values[used_uuid_count]
                used_uuid_count += 1

            previous_code_line = current_code_line
            previous_indentation_level = current_indentation_level
            previous_code_type = current_code_type
        function_dot_codes[function_name] = function_dot_code
    return function_dot_codes

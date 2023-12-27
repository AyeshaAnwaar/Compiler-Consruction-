import re

class SyntaxTreeNode:
    def __init__(self, label, value=None):
        self.label = label
        self.value = value
        self.children = []

def build_syntax_tree(tokens):
    root = SyntaxTreeNode("PROGRAM")
    current_node = root

    for token in tokens:
        if token[0] == "DATATYPE":
            data_type_node = SyntaxTreeNode("DATATYPE", token[1])
            current_node.children.append(data_type_node)
            current_node = data_type_node
        elif token[0] == "IDENTIFIER":
            identifier_node = SyntaxTreeNode("IDENTIFIER", token[1])
            current_node.children.append(identifier_node)
        elif token[0] == "OPERATOR":
            operator_node = SyntaxTreeNode("OPERATOR", token[1])
            current_node.children.append(operator_node)
        elif token[0] == "INTEGER":
            integer_node = SyntaxTreeNode("INTEGER", token[1])
            current_node.children.append(integer_node)
        elif token[0] == "END_STATEMENT":
            current_node = root  # Move back to the root for the next statement

    return root

def perform_semantic_analysis(node):
    if node.label == "DATATYPE":
        current_data_type = node.value
    elif node.label == "OPERATOR":
        if node.value in ['+', '-', '*', '/']:
            # Check if the operands have compatible data types
            left_operand = node.children[0]
            right_operand = node.children[1]

            if left_operand.label == "IDENTIFIER" and right_operand.label == "IDENTIFIER":
                left_data_type = symbol_table[left_operand.value]['data_type']
                right_data_type = symbol_table[right_operand.value]['data_type']

                if left_data_type != right_data_type:
                    print(f"Semantic Error: Incompatible data types in {node.value} operation.")
            elif left_operand.label == "IDENTIFIER" and right_operand.label == "INTEGER":
                left_data_type = symbol_table[left_operand.value]['data_type']
                if left_data_type != "int":
                    print(f"Semantic Error: Incompatible data types in {node.value} operation.")
            elif left_operand.label == "INTEGER" and right_operand.label == "IDENTIFIER":
                right_data_type = symbol_table[right_operand.value]['data_type']
                if right_data_type != "int":
                    print(f"Semantic Error: Incompatible data types in {node.value} operation.")

def print_semantic_tree(node, indent=""):
    print(f"{indent}{node.label}: {node.value}")
    for child in node.children:
        print_semantic_tree(child, indent + "  ")

# Function to calculate First sets
def calculate_first_sets(grammar_rules):
    first_sets = {}

    for rule in grammar_rules:
        non_terminal = rule[0]
        first_set = set()

        for symbol in rule[1:]:
            if symbol in terminals:
                first_set.add(symbol)
                break
            elif symbol in non_terminals:
                first_set |= first_sets[symbol]
                if 'EPSILON' not in first_sets[symbol]:
                    break

        first_sets[non_terminal] = first_set

    return first_sets

# Function to calculate Follow sets
def calculate_follow_sets(grammar_rules, first_sets):
    follow_sets = {non_terminal: set() for non_terminal in non_terminals}
    follow_sets[start_symbol].add('$')  # $ represents end of input

    for rule in grammar_rules:
        for i, symbol in enumerate(rule[1:]):
            if symbol in non_terminals:
                rest = rule[i + 2:]
                first_rest = calculate_first_of_sequence(rest, first_sets)

                follow_sets[symbol] |= (first_rest - {'EPSILON'})

                if 'EPSILON' in first_rest:
                    follow_sets[symbol] |= follow_sets[rule[0]]

    return follow_sets

# Function to calculate First set of a sequence
def calculate_first_of_sequence(sequence, first_sets):
    first_sequence = set()

    for symbol in sequence:
        if symbol in terminals:
            first_sequence.add(symbol)
            break
        elif symbol in non_terminals:
            first_sequence |= first_sets[symbol]
            if 'EPSILON' not in first_sets[symbol]:
                break

    return first_sequence

source_code = '''
#include <iostream>
using namespace std;

int main() {
  int n;

  cout << "Enter an integer: ";
  cin >> n;

  if ( n % 2 == 0)
    cout << n << " is even.";
  else
    cout << n << " is odd.";

  return 0;
}

'''.split()

symbol_table = {}  # Symbol table to store variable information
tokens = []

for word in source_code:
    if word in ['int', 'double', 'float', 'char']:
        tokens.append(['DATATYPE', word])
    elif re.match("[a-zA-Z]+", word):
        identifier = word
        tokens.append(['IDENTIFIER', identifier])

        # Check if the identifier is already in the symbol table
        if identifier in symbol_table:
            print("Error: Variable '{identifier}' redeclaration")
        else:
            # Assume all variables have the same data type for simplicity
            if len(tokens) >= 2:
                data_type = tokens[-2][1]
            else:
                print("Error: Unable to determine data type")
                data_type = None

            symbol_table[identifier] = {'data_type': data_type, 'value': None}

    elif word in ['+', '-', '*', '/', '%', '=']:
        tokens.append(['OPERATOR', word])
    elif re.match("\d+", word):
        # Remove non-numeric characters
        numeric_part = re.sub(r'\D', '', word)

        if numeric_part:
            integer_value = int(numeric_part)
            tokens.append(["INTEGER", integer_value])

            # Check if the word has a semicolon and add an END_STATEMENT token
            if word[-1] == ';':
                tokens.append(['END_STATEMENT', ';'])

# Grammar rules for variable declaration and assignment
grammar_rules = [
    ('DATATYPE', 'IDENTIFIER', 'END_STATEMENT'),  # int result;
    ('DATATYPE', 'IDENTIFIER', 'OPERATOR', 'INTEGER', 'END_STATEMENT'),  # int result = 100;
    ('DATATYPE', 'IDENTIFIER', 'OPERATOR', 'IDENTIFIER', 'END_STATEMENT'),  # int result = otherVar;
    ('DATATYPE', 'IDENTIFIER', 'OPERATOR', 'IDENTIFIER', 'OPERATOR', 'INTEGER', 'END_STATEMENT'),  # int result = otherVar + 100;
     ('DATATYPE', 'IDENTIFIER', 'END_STATEMENT'),                           # int result;
    ('DATATYPE', 'IDENTIFIER', 'OPERATOR', 'INTEGER', 'OPERATOR', 'IDENTIFIER', 'END_STATEMENT'),  # int result = 100 + otherVar;
    ('DATATYPE', 'IDENTIFIER', 'OPERATOR', 'IDENTIFIER', 'OPERATOR', 'INTEGER', 'END_STATEMENT'),  # int result = otherVar + 100;
    ('DATATYPE', 'IDENTIFIER', 'OPERATOR', 'DATATYPE', 'IDENTIFIER', 'END_STATEMENT'),  # int result = int otherVar;
    ('DATATYPE', 'IDENTIFIER', 'OPERATOR', 'DATATYPE', 'IDENTIFIER', 'OPERATOR', 'INTEGER', 'END_STATEMENT'),  # int result = int otherVar + 100;
    ('DATATYPE', 'IDENTIFIER', 'OPERATOR', 'DATATYPE', 'IDENTIFIER', 'OPERATOR', 'DATATYPE', 'IDENTIFIER', 'END_STATEMENT'),  # int result = int var1 + int var2;
    ('DATATYPE', 'IDENTIFIER', 'OPERATOR', 'IDENTIFIER', 'OPERATOR', 'IDENTIFIER', 'END_STATEMENT'),  # int result = var1 + var2;
    ('DATATYPE', 'IDENTIFIER', 'OPERATOR', 'IDENTIFIER', 'OPERATOR', 'INTEGER', 'OPERATOR', 'IDENTIFIER', 'END_STATEMENT'),  # int result = var1 + 100 + var2;
    ('DATATYPE', 'IDENTIFIER', 'OPERATOR', 'IDENTIFIER', 'OPERATOR', 'INTEGER', 'OPERATOR', 'DATATYPE', 'IDENTIFIER', 'END_STATEMENT'),  # int result = var1 + 100 + int var2;
    ('DATATYPE', 'IDENTIFIER', 'OPERATOR', 'IDENTIFIER', 'OPERATOR', 'DATATYPE', 'IDENTIFIER', 'OPERATOR', 'INTEGER', 'END_STATEMENT'),
    ('DATATYPE', 'IDENTIFIER', 'OPERATOR', 'INTEGER', 'END_STATEMENT'),   # int result = 100;
    ('DATATYPE', 'IDENTIFIER', 'OPERATOR', 'IDENTIFIER', 'END_STATEMENT'), # int result = otherVar;
    ('DATATYPE', 'IDENTIFIER', 'OPERATOR', 'INTEGER'),                     # int result = 100
    ('DATATYPE', 'IDENTIFIER', 'END_STATEMENT'),                           # int result;
    ('DATATYPE', 'IDENTIFIER', 'OPERATOR', 'INTEGER', 'OPERATOR', 'INTEGER', 'END_STATEMENT'),
    ('PROGRAM', 'FUNCTION'),  # Function declaration in the program
    ('FUNCTION', 'DATATYPE', 'IDENTIFIER', '(', 'PARAMETERS', ')', '{', 'STATEMENTS', '}'),
    ('PARAMETERS', 'DATATYPE', 'IDENTIFIER', 'PARAMETERS_TAIL'),
    ('PARAMETERS_TAIL', ',', 'DATATYPE', 'IDENTIFIER', 'PARAMETERS_TAIL'),
    ('PARAMETERS_TAIL', 'EPSILON'),
    ('STATEMENTS', 'STATEMENT', 'STATEMENTS'),
    ('STATEMENTS', 'EPSILON'),
    ('STATEMENT', 'DATATYPE', 'IDENTIFIER', 'END_STATEMENT'),  # Variable declaration statement
    ('STATEMENT', 'IDENTIFIER', 'OPERATOR', 'EXPRESSION', 'END_STATEMENT'),  # Assignment statement
    ('STATEMENT', 'IF', '(', 'CONDITION', ')', '{', 'STATEMENTS', '}'),
    ('STATEMENT', 'IF', '(', 'CONDITION', ')', '{', 'STATEMENTS', '}', 'ELSE', '{', 'STATEMENTS', '}'),
    ('CONDITION', 'EXPRESSION', 'COMPARISON_OPERATOR', 'EXPRESSION'),
    ('EXPRESSION', 'TERM', 'EXPRESSION_TAIL'),
    ('EXPRESSION_TAIL', 'ADD_OPERATOR', 'TERM', 'EXPRESSION_TAIL'),
    ('EXPRESSION_TAIL', 'EPSILON'),
    ('TERM', 'FACTOR', 'TERM_TAIL'),
    ('TERM_TAIL', 'MUL_OPERATOR', 'FACTOR', 'TERM_TAIL'),
    ('TERM_TAIL', 'EPSILON'),
    ('FACTOR', 'IDENTIFIER'),
    ('FACTOR', 'INTEGER'),
    ('IF', 'if'),
    ('ELSE', 'else'),
    ('COMPARISON_OPERATOR', '=='),
    ('COMPARISON_OPERATOR', '!='),
    ('COMPARISON_OPERATOR', '<'),
    ('COMPARISON_OPERATOR', '>'),
    ('COMPARISON_OPERATOR', '<='),
    ('COMPARISON_OPERATOR', '>='),
    ('ADD_OPERATOR', '+'),
    ('ADD_OPERATOR', '-'),
    ('MUL_OPERATOR', '*'),
    ('MUL_OPERATOR', '/'),
    
    
]

# Add terminals and non-terminals lists to your code
terminals = ['DATATYPE', 'IDENTIFIER', 'OPERATOR', 'INTEGER', 'END_STATEMENT']
non_terminals = ['PROGRAM', 'DATATYPE', 'IDENTIFIER', 'OPERATOR', 'INTEGER', 'END_STATEMENT']

# Add the start symbol
start_symbol = 'PROGRAM'

# Calculate First and Follow sets
first_sets = calculate_first_sets(grammar_rules)
follow_sets = calculate_follow_sets(grammar_rules, first_sets)

# Print First and Follow sets
print("\nFirst Sets:")
for non_terminal, first_set in first_sets.items():
    print(f"{non_terminal}: {first_set}")

print("\nFollow Sets:")
for non_terminal, follow_set in follow_sets.items():
    print(f"{non_terminal}: {follow_set}")

# Build the syntax tree
syntax_tree = build_syntax_tree(tokens)
perform_semantic_analysis(syntax_tree)

# Function to print the syntax tree (depth-first traversal)
def print_syntax_tree(node, level=0):
    print("  " * level + f"{node.label}: {node.value}")
    for child in node.children:
        print_syntax_tree(child, level + 1)

# Print the syntax tree
print("\nSyntax Tree:")
print_syntax_tree(syntax_tree)
# Print the syntax tree
print("----------------------------------------------------------------------------------")
print("\n")
print("Semantic Analysis Tree:")
print_semantic_tree(syntax_tree)
print("----------------------------------------------------------------------------------")
print("\n")
print("Tokens are:: ")
print(tokens)

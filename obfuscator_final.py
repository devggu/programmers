import ast
import random
import re

class ObfuscateVariables(ast.NodeTransformer):
    def __init__(self):
        self.names_map = {}
        self.used_names = set()  # search for used names

    def random_name(self, length=17):
        while True:
            name = 'O' + ''.join(random.choice(['O', '0']) for _ in range(length - 1)) + ' '
            if name not in self.used_names:
                self.used_names.add(name)
                return name

    def visit_FunctionDef(self, node):
        # obfuscate function parameters
        for arg in node.args.args:
            param_name = arg.arg
            obfuscated_name = self.random_name()
            self.names_map[param_name] = obfuscated_name
            arg.arg = obfuscated_name

        self.generic_visit(node)
        return node

    def visit_Assign(self, node):
        # variable allocation obfuscation
        for target in node.targets:
            if isinstance(target, ast.Name):
                var_name = target.id
                if var_name not in self.names_map:
                    self.names_map[var_name] = self.random_name()
                target.id = self.names_map[var_name]
        self.generic_visit(node)
        return node

    def visit_Name(self, node):
        # variable usage obfuscation
        if node.id in self.names_map:
            node.id = self.names_map[node.id]
        return node

def remove_comments_and_docstrings(source):
    # remove comments and docstrings
    return re.sub(r"#.*|\n\s*('''[\s\S]*?'''|\"\"\"[\s\S]*?\"\"\")", '', source, flags=re.MULTILINE)

def remove_empty_lines(source_code):
    lines = source_code.split('\n')
    non_empty_lines = [line for line in lines if line.strip() != '']
    return '\n'.join(non_empty_lines)

def obfuscate_file(input_file_path, output_file_path):
    with open(input_file_path, 'r') as file:
        source_code = file.read()

    source_code_no_comments = remove_comments_and_docstrings(source_code)

    tree = ast.parse(source_code_no_comments)
    obfuscator = ObfuscateVariables()
    obfuscated_tree = obfuscator.visit(tree)
    obfuscated_code = ast.unparse(obfuscated_tree)

    obfuscated_code_no_empty_lines = remove_empty_lines(obfuscated_code)
    
    with open(output_file_path, 'w') as file:
        file.write(obfuscated_code_no_empty_lines)

if __name__ == '__main__':
    input_file_path = input('Input file path: ')
    output_file_path = input('Output file path: ')

    obfuscate_file(input_file_path, output_file_path)

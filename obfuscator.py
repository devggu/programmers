import ast
import random
import re

class RenameVariablesAndAttributes(ast.NodeTransformer):
    def __init__(self):
        self.names_map = {}
        self.declared_vars = set()
        self.self_attributes = set()

    def random_name(self, length=15):
        return 'O' + ''.join(random.choice(['O', '0']) for _ in range(length - 1)) + ' '

    def obfuscate_self_attributes(self, node):
        if isinstance(node, ast.Attribute) and isinstance(node.value, ast.Name) and node.value.id == 'self':
            attr = node.attr
            if attr not in self.self_attributes:
                self.self_attributes.add(attr)
                self.names_map[attr] = self.random_name()
            node.attr = self.names_map[attr]

    def visit_FunctionDef(self, node):
        # Obfuscate function parameters
        for arg in node.args.args:
            param_name = arg.arg
            if param_name not in self.names_map:
                self.names_map[param_name] = self.random_name()
            arg.arg = self.names_map[param_name]
        self.generic_visit(node)
        return node

    def visit_Assign(self, node):
        for target in node.targets:
            self.obfuscate_self_attributes(target)
        self.generic_visit(node)
        return node

    def visit_Attribute(self, node):
        self.obfuscate_self_attributes(node)
        return node

    def visit_Name(self, node):
        if node.id in self.declared_vars and node.id in self.names_map:
            node.id = self.names_map[node.id]
        return node

def remove_comments_and_docstrings(source):
    return re.sub(r"#.*|\n\s*('''[\s\S]*?'''|\"\"\"[\s\S]*?\"\"\")", '', source, flags=re.MULTILINE)

def obfuscate_file(input_file_path, output_file_path):
    with open(input_file_path, 'r') as file:
        source_code = file.read()

    source_code_no_comments = remove_comments_and_docstrings(source_code)

    tree = ast.parse(source_code_no_comments)
    transformer = RenameVariablesAndAttributes()
    transformer.visit(tree)
    obfuscated_code = ast.unparse(tree)

    with open(output_file_path, 'w') as file:
        file.write(obfuscated_code)

if __name__ == '__main__':
    input_file_path = input('Press Enter to obfuscate the file:\n')
    output_file_path = input_file_path[:-3]+'_obf.py'

    obfuscate_file(input_file_path, output_file_path)

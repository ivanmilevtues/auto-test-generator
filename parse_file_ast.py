import ast

def get_ast(filename="TestableClass.py"):
    source = ''
    with open(filename, 'r') as f:
        source = ''.join(f.readlines())

    ast_parse = ast.parse(source)
    return ast.dump(ast_parse)

if __name__ == "__main__":
    print(get_ast("TestTestableClass.py"))
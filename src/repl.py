import json
from frontend.parser import Parser, Program
from runtime.values import RuntimeVal
from runtime.interpreter import Interpreter
from runtime.environment import create_global_env

def print_tree(node, indent=0):
    if isinstance(node, dict):
        for key, value in node.items():
            if isinstance(value, (dict, list)):
                print("  " * indent + f"{key}:")
                print_tree(value, indent + 1)
            else:
                try:
                    serialized_value = json.dumps(value)
                    print("  " * indent + f"{key}: {serialized_value}")
                except TypeError:
                    print("  " * indent + f"{key}: [Non-serializable]")
    elif isinstance(node, list):
        for item in node:
            if isinstance(item, (dict, list)):
                print_tree(item, indent)
            else:
                try:
                    serialized_item = json.dumps(item)
                    print("  " * indent + f"- {serialized_item}")
                except TypeError:
                    print("  " * indent + "- [Non-serializable]")


def repl() :

    print('\nNanoScript v0.1\n')

    # global env since we want to persist the env across the entire repl session
    env = create_global_env()
    
    while(True) :
        inp = input('>> ').strip()
        if(inp == '' or inp == 'exit') :
            exit(0)
        
        parser = Parser()

        program : Program = parser.generate_ast(inp)
        interpreter = Interpreter(env)
       
        result : RuntimeVal = interpreter.evaluate(program)
        print(result.__dict__)

def run() :

    print('\nNanoScript v0.1\n')

    # global env since we want to persist the env across the entire repl session
    env = create_global_env()
    
    f = open('./../tests/test.txt', 'r')
    inp = f.read()
    f.close()
    
    print()
    print(inp)
    print()

    parser = Parser()

    program : Program = parser.generate_ast(inp)
    print_tree(program.body)
    
    interpreter = Interpreter(env)
    
    result : RuntimeVal = interpreter.evaluate(program)
    print(result.__dict__)



if __name__ == '__main__' :

    # repl()
    run()



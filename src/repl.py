from frontend.parser import Parser, Program
from runtime.values import RuntimeVal
from runtime.interpreter import Interpreter
from runtime.environment import create_global_env

def repl() :

    print("\nNanoScript v0.1\n")

    # global env since we want to persist the env across the entire repl session
    env = create_global_env()
    
    while(True) :
        inp = input(">> ").strip()
        if(inp == "" or inp == "exit") :
            exit(0)
        
        parser = Parser()

        program : Program = parser.generate_ast(inp)
        interpreter = Interpreter(env)
       
        result : RuntimeVal = interpreter.evaluate(program)
        print(result.__dict__)

def run() :

    print("\nNanoScript v0.1\n")

    # global env since we want to persist the env across the entire repl session
    env = create_global_env()
    
    f = open('./../tests/test.txt', 'r')
    inp = f.read()
    f.close()
    
    print(inp.replace('\n', ' '))
    print()

    parser = Parser()

    program : Program = parser.generate_ast(inp)
    interpreter = Interpreter(env)
    
    result : RuntimeVal = interpreter.evaluate(program)
    print(result.__dict__)



if __name__ == "__main__" :

    # repl()
    run()



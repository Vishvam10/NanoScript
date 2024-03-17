import json
from frontend.parser import Parser
from runtime.values import NumberVal
from runtime.interpreter import evaluate

def repl() :

    print("\nNanoScript v0.1\n")

    while(True) :

        inp = input().strip()
        if(inp == "" or inp == "exit") :
            exit(0)
        
        parser = Parser()
        program = parser.generate_ast(inp)
        
        print(program.body)

        result = evaluate(program)
        print(result.__dict__)

if __name__ == "__main__" :

    repl()



import json
from frontend.parser import Parser

def repl() :

    parser = Parser()
    print("\nNanoScript v0.1\n")

    while(True) :

        inp = input().strip()
        if(inp == "" or inp == "exit") :
            exit(0)
        
        program = parser.generate_ast(inp)
        
        print(program.body)
        

if __name__ == "__main__" :

    repl()



import json
from frontend.parser import Parser, Program
from runtime.values import RuntimeVal, make_null, make_number, make_bool
from runtime.interpreter import evaluate
from runtime.environment import Environment

def repl() :

    print("\nNanoScript v0.1\n")

    while(True) :

        inp = input().strip()
        if(inp == "" or inp == "exit") :
            exit(0)
        
        parser = Parser()
        env = Environment()
        env.decl_var("x", make_number(100), False)
        env.decl_var("true", make_bool(True), False)
        env.decl_var("false", make_bool(False), False)
        env.decl_var("null", make_null(), False)

        program : Program = parser.generate_ast(inp)
        print(program.body)
        
        result : RuntimeVal = evaluate(program, env)
        print(result.__dict__)

if __name__ == "__main__" :

    repl()



from frontend.parser import Parser, Program
from runtime.values import RuntimeVal, make_null, make_number, make_bool
from runtime.interpreter import Interpreter
from runtime.environment import Environment

def repl() :

    print("\nNanoScript v0.1\n")

    # global env since we want to persist the env across the entire repl session
    env = Environment()
    
    # few global keywords (kinda hacky to set it this way since it bypasses the lexer and the parser)
    env.decl_var("true", make_bool(True), True)
    env.decl_var("false", make_bool (False), True)
    env.decl_var("null", make_null(), True)
    
    while(True) :
        inp = input(">> ").strip()
        if(inp == "" or inp == "exit") :
            exit(0)
        
        parser = Parser()

        program : Program = parser.generate_ast(inp)
        interpreter = Interpreter(env)
       
        result : RuntimeVal = interpreter.evaluate(program)
        print(result.__dict__)


if __name__ == "__main__" :

    repl()



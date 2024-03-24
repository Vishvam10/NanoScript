from typing import Dict, Set, Optional
from runtime.values.base import RuntimeVal

from .values.make import make_bool, make_null, make_number, make_native_fn

# This is the 'scope'. 

class Environment() :

    def __init__(self, parent : Optional['Environment'] = None) -> None:
        self.global_scope : bool = (parent == None)
        self.parent : Environment = None
        self.variables : Dict[
            str, RuntimeVal
        ] = {}
        self.constants : Set[str] = set()
    
    def decl_var(self, var_name : str, value : RuntimeVal, constant : bool) -> RuntimeVal :

        if(var_name in self.variables) :
            print(f'Cannot declare variable {var_name} as it already exists')
            exit(0)

        if(constant) :
            self.constants.add(var_name)

        self.variables[var_name] = value

        return value

    def assign_var(self, var_name : str, value : RuntimeVal) -> RuntimeVal :

        env : Environment = self.resolve(var_name)

        if(var_name in env.constants) :
            print(f'Cannot re-assign to {var_name} as it is a constant')
            exit(0)

        env.variables[var_name] = value

        return value

    def lookup_var(self, var_name : str) -> RuntimeVal :
        
        env : Environment = self.resolve(var_name)
        return env.variables[var_name]

    def resolve(self, var_name : str) -> 'Environment' :
        if(var_name in self.variables) :
            return self
        
        if(self.parent == None) :
            print(f'Cannot resolve {var_name} as it does not exist')
            exit(0)

        return self.parent.resolve(var_name)

def create_global_env() :

    env = Environment()

    # few global keywords (kinda hacky to set it this way since it bypasses the lexer and the parser)
    env.decl_var("true", make_bool(True), True)
    env.decl_var("false", make_bool (False), True)
    env.decl_var("null", make_null(), True)

    # define a native methods :
    
    def print_callback(args, env) :
        print('\n********** CUSTOM PRINT CALLBACK **********\n')
        print(*args)
        print('\n*******************************************\n')
        return make_number(1000000)
    
    env.decl_var('print', make_native_fn(print_callback), True)
    
    return env

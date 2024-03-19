from typing import Dict, Set

from runtime.values import RuntimeVal

# This is the 'scope'. 

class Environment() :

    def __init__(self) -> None:
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






from typing import Dict, Set

from runtime.values import RuntimeVal

# this is the 'scope' 
class Environment() :

    def __init__(self) -> None:
        self.parent : Environment = None
        self.variables : Dict[
            str, RuntimeVal
        ] = {}
        self.constants : Set[str] = set()
    
    def decl_var(self, var_name : str, value : RuntimeVal, constant : bool) -> RuntimeVal :

        if(var_name in self.variables) :
            raise f'Cannot declare variable {var_name} as it already exists'

        if(constant) :
            self.constants.add(var_name)

        self.variables[var_name] = value
        return value

    def assign_var(self, var_name : str, value : RuntimeVal) -> RuntimeVal :

        env : Environment = self.resolve(var_name)

        if(var_name in env.constants) :
            raise f'Cannot re-assign to {var_name} as it is a constant'


        env.variables[var_name] = value

        return value

    def lookup_var(self, var_name : str) -> RuntimeVal :
        
        env : Environment = self.resolve(var_name)
        return env.variables[var_name]

    def resolve(self, var_name : str) -> 'Environment' :
        
        if(var_name in self.variables) :
            return self
        
        if(self.parent == None) :
            raise f'Cannot resolve {var_name} as it does not exist'
    
        return self.parent.resolve(var_name)






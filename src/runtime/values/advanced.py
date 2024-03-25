from typing import List
from .base import RuntimeVal, ValueType

from frontend.ast import Stmt
from ..environment import Environment

class FunctionVal(RuntimeVal) :

    # TODO : make callback of type : 
    # Callabale[[List[RuntimeVal, Environment]], None]
    # current design prevents importing Environment due 
    # to circular nature. Need some refactoring
    def __init__(self, name : str, parameters : List[str], body : List[Stmt], decl_env : Environment):
        super().__init__(ValueType.Function)
        self.name = name
        self.parameters = parameters
        self.body = body
        self.decl_env = decl_env

    def to_dict(self):
        return {'type': self.type, 'name' : self.name, 'parameters' : self.parameters, 'body' : self.body, 'decl_env' : self.decl_env }
    


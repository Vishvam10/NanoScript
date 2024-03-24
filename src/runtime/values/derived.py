from typing import Dict, Callable
from .base import RuntimeVal, ValueType

class NullVal(RuntimeVal) :
    def __init__(self):
        super().__init__(ValueType.Null)
        self.value = None

    def to_dict(self):
        return {'type': self.type}

class BooleanVal(RuntimeVal) :
    def __init__(self, value : bool):
        super().__init__(ValueType.Boolean)
        self.value = value

    def to_dict(self):
        return {'type': self.type}


class NumberVal(RuntimeVal) :
    def __init__(self, value : float):
        super().__init__(ValueType.Number)
        self.value = value

    def to_dict(self):
        return {'type': self.type, 'value' : self.value }
    
class ObjectVal(RuntimeVal) :
    def __init__(self, properties : Dict[str, RuntimeVal]):
        super().__init__(ValueType.Object)
        self.properties = properties

    def to_dict(self):
        return {'type': self.type, 'value' : self.value }

class NativeFunctionVal(RuntimeVal) :

    # TODO : make callback of type : 
    # Callabale[[List[RuntimeVal, Environment]], None]
    # current design prevents importing Environment due 
    # to circular nature. Need some refactoring
    def __init__(self, callback : Callable[..., None]):
        super().__init__(ValueType.NativeFunction)
        self.callback = callback

    def to_dict(self):
        return {'type': self.type, 'callback' : self.callback }
    


# contains values that are need during run time

from enum import Enum
from abc import ABC

class ValueType(Enum):
    Null = "null"
    Number = "number"
    Boolean = "boolean"

class RuntimeVal(ABC):
    def __init__(self, type: ValueType):
        self.type = type

    def to_dict(self):
        return {'type': self.type}

class NullVal(RuntimeVal) :
    def __init__(self):
        super().__init__(ValueType.Null)
        self.value = None

    def to_dict(self):
        return {'type': self.type}

class Boolean(RuntimeVal) :
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
    
      
# sorta like C macros

def make_number(n : float = 0) -> NumberVal :
    return NumberVal(
        value=n
    )

def make_null() -> NullVal :
    return NullVal()

def make_bool(val : bool = True) :
    return Boolean(
        value=val
    )


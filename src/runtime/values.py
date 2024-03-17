# contains values that are need during run time

from enum import Enum
from abc import ABC

class ValueType(Enum):
    Null = "null"
    Number = "number"

class RuntimeVal(ABC):
    def __init__(self, type: ValueType):
        self.type = type

    def to_dict(self):
        return {'type': self.type}

class NullVal(RuntimeVal) :
    def __init__(self):
        super().__init__(ValueType.Null)

    def to_dict(self):
        return {'type': self.type}

class NumberVal(RuntimeVal) :
    def __init__(self, value : float):
        super().__init__(ValueType.Number)
        self.value = value

    def to_dict(self):
        return {'type': self.type, 'value' : self.value }
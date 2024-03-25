# contains values that are need during run time
from typing import Dict
from enum import Enum
from abc import ABC

class ValueType(Enum):
    Null = "null"
    Number = "number"
    Boolean = "boolean"
    Object = "object"
    NativeFunction = "native-function"
    Function = "function"

class RuntimeVal(ABC):
    def __init__(self, type: ValueType):
        self.type = type

    def to_dict(self):
        return {'type': self.type.value}

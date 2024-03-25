from typing import List, Optional
from enum import Enum
from abc import ABC

class NodeType(Enum):

    # Statements
    Stmt = "Statement"
    Program = "Program"
    VariableDecl = "VariableDecl"
    FunctionDecl = "FunctionDecl"

    # Expressions
    AssignmentExpr = "AssignmentExpr"
    BinaryExpr = "BinaryExpr"
    MemberExpr = "MemberExpr"
    CallExpr = "CallExpr"

    # Literals
    Identifier = "Identifier"
    NumericalLiteral = "NumericLiteral"
    PropertyLiteral = "PropertyLiteral"
    ObjectLiteral = "ObjectLiteral" 


# ------------------------------------------------------------------------------
# Statements 
# ------------------------------------------------------------------------------

class Stmt(ABC):
    def __init__(self, kind: NodeType):
        self.kind = kind

    def to_dict(self):
        return {'kind': self.kind.value}

class Program(Stmt):
    def __init__(self):
        super().__init__(NodeType.Program)
        self.body: List[Stmt] = []

    def to_dict(self):
        body = [stmt.to_dict() for stmt in self.body]
        return {'kind': self.kind.value, 'body': body}

class VariableDecl(Stmt):
    def __init__(self, identifier: str, value: 'Expr', constant: bool) -> None:
        super().__init__(NodeType.VariableDecl)
        self.identifier = identifier
        self.value = value 
        self.constant = constant

    def to_dict(self):
        # print('REACHED : ', self.value)
        value = self.value.to_dict() if self.value is not None else None
        return {'kind': self.kind.value, 'identifier': self.identifier, 'value': value, 'constant': self.constant}

class FunctionDecl(Stmt):
    def __init__(self, name : str, parameters: List[str], body : List[Stmt]) -> None:
        super().__init__(NodeType.FunctionDecl)
        self.name = name
        self.parameters = parameters
        self.body = body

    def to_dict(self):
        body = [stmt.to_dict() for stmt in self.body]
        return {'kind': self.kind.value, 'name': self.name, 'parameters': self.parameters, 'body': body}

# ------------------------------------------------------------------------------
# Expressions 
# ------------------------------------------------------------------------------

class Expr(Stmt):
    def __init__(self, kind: NodeType):
        super().__init__(kind)

class BinaryExpr(Expr):
    def __init__(self, left: Expr, right: Expr, operator: str):
        super().__init__(NodeType.BinaryExpr)
        self.left = left
        self.right = right
        self.operator = operator

    def to_dict(self):
        return {'kind': self.kind.value, 'left': self.left.to_dict(), 'right': self.right.to_dict(), 'operator': self.operator}

class AssignmentExpr(Expr):
    def __init__(self, assignee : Expr, value : Expr):
        super().__init__(NodeType.AssignmentExpr)

        # assignee is not an Identifier because things like obj.property are not a valid Identifier. It is a different type of Expr which is much more complex to handle
        self.assignee = assignee
        self.value = value

    def to_dict(self):
        value = self.value.to_dict() if self.value is not None else None
        return {'kind': self.kind.value, 'assignee': self.assignee.to_dict(), 'value': value}

class Identifier(Expr):
    def __init__(self, symbol: str):
        super().__init__(NodeType.Identifier)
        self.symbol = symbol

    def to_dict(self):
        return {'kind': self.kind.value, 'symbol': self.symbol}

class CallExpr(Expr):
    def __init__(self, args : List[Expr], caller : Expr):
        super().__init__(NodeType.CallExpr)
        self.args = args
        
        # not Identifier because of cases like this : foo.bar() 
        self.caller = caller

    def to_dict(self):
        args = [arg.to_dict() for arg in self.args]
        return {'kind': self.kind.value, 'args' : args, 'caller' : self.caller.to_dict()}

class MemberExpr(Expr):
    def __init__(self, object: Expr, property : Expr, computed : bool):
        super().__init__(NodeType.MemberExpr)
        self.object = object
        self.property = property

        # for cases like foo["bar"]() or foo[baz()]()
        self.computed = computed

    def to_dict(self):
        return {'kind': self.kind.value, 'object' : self.object.to_dict(), 'property' : self.property.to_dict(), 'computed' : self.computed}


# ------------------------------------------------------------------------------
# Literals 
# ------------------------------------------------------------------------------


class NumericLiteral(Expr):
    def __init__(self, value: float):
        super().__init__(NodeType.NumericalLiteral)
        self.value = value

    def to_dict(self):
        return {'kind': self.kind.value, 'value': self.value}

class PropertyLiteral(Expr):
    def __init__(self, key : str, value : Optional[Expr] = None):
        super().__init__(NodeType.PropertyLiteral)
        self.key = key
        self.value = value

    def to_dict(self):
        value = self.value.to_dict() if self.value is not None else None
        return {'kind': self.kind.value, 'value': self.value.to_dict()}

class ObjectLiteral(Expr):
    def __init__(self, properties: List[PropertyLiteral]):
        super().__init__(NodeType.ObjectLiteral)
        self.properties = properties

    def to_dict(self):
        properties = [prop.to_dict() for prop in self.properties]
        return {'kind': self.kind.value, 'properties': properties}

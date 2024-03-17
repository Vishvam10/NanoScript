import json
from typing import List
from enum import Enum, auto
from abc import ABC, ABCMeta


class NodeType(Enum):

    # Statements
    Stmt = "Statement"
    Program = "Program"
    VariableDecl = "VariableDecl"

    # Expressions
    Expr = "Expr"
    BinaryExpr = "BinaryExpr"
    Identifier = "Identifier"
    NumericalLiteral = "NumericLiteral"


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
        return {'kind': self.kind.value, 'body': [stmt.to_dict() for stmt in self.body]}


class VariableDecl(Stmt):
    def __init__(self, identifier: str, value: 'Expr', constant: bool) -> None:
        super().__init__(NodeType.VariableDecl)
        self.identifier = identifier
        self.value = value 
        self.constant = constant

    def to_dict(self):
        return {'kind': self.kind.value, 'indentifier': self.identifier, 'value': self.value, 'constant': self.constant}


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


class NumericLiteral(Expr):
    def __init__(self, value: float):
        super().__init__(NodeType.NumericalLiteral)
        self.value = value

    def to_dict(self):
        return {'kind': self.kind.value, 'value': self.value}

class Identifier(Expr):
    def __init__(self, symbol: str):
        super().__init__(NodeType.Identifier)
        self.symbol = symbol

    def to_dict(self):
        return {'kind': self.kind.value, 'symbol': self.symbol}

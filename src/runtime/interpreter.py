from typing import cast

from .values import *
from frontend.ast import *
from runtime.environment import Environment

class Interpreter() :

    def __init__(self, env : Environment) -> None:
        self.env = env
        return

    def _evaluate_numeric_binary_expr(self, left: NumberVal, right: NumberVal, operator: str) -> NumberVal:

        res = 0

        if (operator == '+'):
            res = left.value + right.value
        elif (operator == '-'):
            res = left.value - right.value
        elif (operator == '*'):
            res = left.value * right.value
        elif (operator == '/'):
            if (right.value != 0):
                res = left.value / right.value
            else:
                print('\n[INTERPRETER ERROR] : Division by 0')
                exit(0)
        elif (operator == '%'):
            res = left.value % right.value

        return make_number(res)

    def _evaluate_binary_expr(self, expr: BinaryExpr) -> RuntimeVal:

        left = self.evaluate(expr.left)
        right = self.evaluate(expr.right)

        if (isinstance(left, NumberVal) and isinstance(right, NumberVal)):
            return self._evaluate_numeric_binary_expr(left, right, expr.operator)

        return make_null()

    def _evaluate_identifier(self, ident: Identifier) -> RuntimeVal:

        val = self.env.lookup_var(ident.symbol)
        return val

    def _evaluate_object_expr(self, obj : ObjectLiteral) -> RuntimeVal :
        
        res = ObjectVal({})

        for prop in obj.properties :
            value = self.evaluate(prop.value) if (prop.value) else self.env.lookup_var(prop.key)

            res.properties[prop.key] = value
        return res

    def _evaluate_variable_decl(self, decl: VariableDecl) -> RuntimeVal:

        val = make_null()

        if (decl.value):
            val = self.evaluate(decl.value)
        
        return self.env.decl_var(var_name=decl.identifier, value=val, constant=decl.constant)

    def _evaluate_assignment(self, node : AssignmentExpr) :

        if(node.assignee.kind != NodeType.Identifier) :
            print(f'\n[INTERPRETER ERROR] : Invalid LHS inside assignmenr expr : {node.assignee.to_dict()}')
            exit(0)
        
        var_name = cast(Identifier, node.assignee).symbol
        value = self.evaluate(node.value)
       
        return self.env.assign_var(var_name, value)

    def _evaluate_program(self, program: Program) -> RuntimeVal:

        last_evaluated: RuntimeVal = make_null()

        for stmt in program.body:
            last_evaluated = self.evaluate(stmt)

        return last_evaluated

    def evaluate(self, ast_node: Stmt) -> RuntimeVal:

        if (ast_node == None):
            print('\n[INTERPRETER ERROR] : AST node is None : ', ast_node)
            exit(0)

        if (ast_node.kind == NodeType.NumericalLiteral):
            return NumberVal(value=ast_node.value)
        
        elif(ast_node.kind == NodeType.AssignmentExpr) :
            return self._evaluate_assignment(ast_node)

        elif (ast_node.kind == NodeType.BinaryExpr):
            return self._evaluate_binary_expr(ast_node)

        elif (ast_node.kind == NodeType.Identifier):
            return self._evaluate_identifier(ast_node)
        
        elif (ast_node.kind == NodeType.ObjectLiteral):
            return self._evaluate_object_expr(ast_node)

        elif (ast_node.kind == NodeType.VariableDecl):
            return self._evaluate_variable_decl(ast_node)

        elif (ast_node.kind == NodeType.Program):
            return self._evaluate_program(ast_node)

        else:
            print('\n[INTERPRETER ERROR] :  This AST node has not been yet been setup for interpretation : ', ast_node.to_dict())
            exit(0)

        
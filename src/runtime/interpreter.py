from typing import cast

from .values import ValueType, RuntimeVal, NumberVal, make_null, make_number
from frontend.ast import NodeType, Stmt, Identifier, VariableDecl, AssignmentExpr, BinaryExpr, Program
from runtime.environment import Environment


def _evaluate_numeric_binary_expr(left: NumberVal, right: NumberVal, operator: str) -> NumberVal:

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
            print('[INTERPRETER ERROR] : Division by 0')
    elif (operator == '%'):
        res = left.value % right.value

    return make_number(res)


def _evaluate_binary_expr(expr: BinaryExpr, env: Environment) -> RuntimeVal:

    left = evaluate(expr.left, env)
    right = evaluate(expr.right, env)

    if (isinstance(left, NumberVal) and isinstance(right, NumberVal)):
        return _evaluate_numeric_binary_expr(left, right, expr.operator)

    return make_null()


def _evaluate_identifier(ident: Identifier, env: Environment) -> RuntimeVal:

    val = env.lookup_var(ident.symbol)
    return val


def _evaluate_variable_decl(decl: VariableDecl, env: Environment) -> RuntimeVal:

    val = make_null()

    if (decl.value):
        val = evaluate(decl.value, env)

    return env.decl_var(var_name=decl.identifier, value=val, constant=decl.constant)

def _evaluate_assignment(node : AssignmentExpr, env : Environment) :

    if(not isinstance(node.assignee.kind, Identifier)) :
        print(f'[INTERPRETER ERROR] : Invalid LHS inside assignmenr expr : {node.assignee.to_dict()}')
    
    var_name = cast(Identifier, node.assignee).symbol
    value = evaluate(node.value, env)
    env.assign_var(var_name, value)

def _evaluate_program(program: Program, env: Environment) -> RuntimeVal:

    last_evaluated: RuntimeVal = make_null()

    for stmt in program.body:
        last_evaluated = evaluate(stmt, env)

    return last_evaluated


def evaluate(ast_node: Stmt, env: Environment) -> RuntimeVal:

    print('ast node : ', ast_node)

    if (ast_node == None):
        print('[INTERPRETER ERROR] : AST node is None : ', ast_node)
        exit(0)

    if (ast_node.kind == NodeType.NumericalLiteral):
        return NumberVal(value=ast_node.value)
    
    elif(ast_node.kind == NodeType.AssignmentExpr) :
        return _evaluate_assignment(ast_node, env)

    elif (ast_node.kind == NodeType.BinaryExpr):
        return _evaluate_binary_expr(ast_node, env)

    elif (ast_node.kind == NodeType.Identifier):
        return _evaluate_identifier(ast_node, env)

    elif (ast_node.kind == NodeType.VariableDecl):
        return _evaluate_variable_decl(ast_node, env)

    elif (ast_node.kind == NodeType.Program):
        return _evaluate_program(ast_node, env)

    else:
        print('[INTERPRETER ERROR] :  This AST node has not been yet been setup for interpretation : ', ast_node.to_dict())
        exit(0)

from .values import ValueType, RuntimeVal, NumberVal, make_null, make_number
from frontend.ast import NodeType, Stmt, Identifier, BinaryExpr, Program
from runtime.environment import Environment

def _evaluate_numeric_binary_expr(left : NumberVal, right : NumberVal, operator : str) -> NumberVal :
    
    res = 0

    if(operator == '+') :
        res = left.value + right.value
    elif(operator == '-') :
        res = left.value - right.value
    elif(operator == '*') :
        res = left.value * right.value
    elif(operator == '/') :
        if(right.value != 0) :
            res = left.value / right.value
        else :
            print('[INTERPRETER ERROR] : Division by 0')
    elif(operator == '%') :
        res = left.value % right.value

    return make_number(res)


def _evaluate_binary_expr(expr : BinaryExpr, env : Environment) -> RuntimeVal :

    left = evaluate(expr.left, env)
    right = evaluate(expr.right, env)

    if(isinstance(left, NumberVal) and isinstance(right, NumberVal)) :
        return _evaluate_numeric_binary_expr(left, right, expr.operator)

    return make_null()

def _evaluate_identifier(ident : Identifier, env : Environment) -> RuntimeVal :

    val = env.lookup_var(ident.symbol)
    return val 

def _evaluate_program(program : Program, env : Environment) -> RuntimeVal :

    last_evaluated : RuntimeVal = make_null()

    for stmt in program.body :
        last_evaluated = evaluate(stmt, env)
        print('in program : ', stmt.kind, last_evaluated)

    return last_evaluated

def evaluate(ast_node : Stmt, env : Environment) -> RuntimeVal :
    print('\neval : ', ast_node.kind)
    if(ast_node.kind == NodeType.NumericalLiteral) :
        return NumberVal(
            value=ast_node.value
        )

    elif(ast_node.kind == NodeType.BinaryExpr) :
        return _evaluate_binary_expr(ast_node, env)

    elif(ast_node.kind == NodeType.Identifier) :
        return _evaluate_identifier(ast_node, env)

    elif(ast_node.kind == NodeType.Program) :
        return _evaluate_program(ast_node, env)

    else :
        print("[INTERPRETER ERROR] :  This AST node has not been yet been setup for interpretation")




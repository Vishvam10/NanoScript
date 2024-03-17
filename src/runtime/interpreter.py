from .values import ValueType, RuntimeVal, NumberVal, NullVal
from frontend.ast import NodeType, Stmt, BinaryExpr, Program

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

    return NumberVal(
        value=res
    )


def _evaluate_binary_expr(expr : BinaryExpr) -> RuntimeVal :

    left = evaluate(expr.left)
    right = evaluate(expr.right)

    if(isinstance(left, NumberVal) and isinstance(right, NumberVal)) :
        return _evaluate_numeric_binary_expr(left, right, expr.operator)

    return NullVal()

def _evaluate_program(program : Program) -> RuntimeVal :

    last_evaluated : RuntimeVal = NullVal()

    for stmt in program.body :
        last_evaluated = evaluate(stmt)
        print('in program : ', stmt.kind, last_evaluated)

    return last_evaluated

# we will be evaluating the nodes and will
# be getting the runtime values
def evaluate(ast_node : Stmt) -> RuntimeVal :
    print('\neval : ', ast_node.kind)
    if(ast_node.kind == NodeType.NumericalLiteral) :
        return NumberVal(
            value=ast_node.value
        )

    elif(ast_node.kind == NodeType.BinaryExpr) :
        return _evaluate_binary_expr(ast_node)

    elif(ast_node.kind == NodeType.NullLiteral) :
        return NullVal()

    elif(ast_node.kind == NodeType.Program) :
        return _evaluate_program(ast_node)

    else :
        print("[INTERPRETER ERROR] :  This AST node has not been yet been setup for interpretation")




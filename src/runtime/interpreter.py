import json
from typing import cast

from frontend.ast import *
from .values.base import *
from .values.derived import ObjectVal, NumberVal
from .values.advanced import FunctionVal
from .values.make import make_null, make_number
from .environment import Environment

'''

    - by default, we assign the global env to the interpreter
    - we will need to pass in env in almost every evaluate method because
      functions have it's own scope and we need to tell the interpreter
      which env to work with while evaluating it

'''

class Interpreter() :

    def __init__(self, env : Environment) -> None:
        self.global_env = env
        return

    def _evaluate_numeric_binary_expr(self, left: NumberVal, right: NumberVal, operator: str, env : Environment) -> NumberVal:

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

    def _evaluate_binary_expr(self, expr: BinaryExpr, env: Environment) -> RuntimeVal :

        left = self.evaluate(expr.left, env)
        right = self.evaluate(expr.right, env)

        if (isinstance(left, NumberVal) and isinstance(right, NumberVal)):
            return self._evaluate_numeric_binary_expr(left, right, expr.operator, env)

        return make_null()

    def _evaluate_identifier(self, ident: Identifier, env : Environment) -> RuntimeVal :

        val = env.lookup_var(ident.symbol)
        return val

    def _evaluate_object_expr(self, obj : ObjectLiteral, env : Environment) -> RuntimeVal :
        
        res = ObjectVal({})

        for prop in obj.properties :

            # to handle { foo } which is the same as { foo : foo }
            value = self.evaluate(prop.value, env) if (prop.value) else env.lookup_var(prop.key)

            res.properties[prop.key] = value

        return res

    def _evaluate_call_expr(self, expr : CallExpr, env : Environment) -> RuntimeVal :
        
        args : List[RuntimeVal] = []

        for arg in expr.args :
            value = self.evaluate(arg, env)
            args.append(value)
        
        func = self.evaluate(expr.caller, env)

        if(func.type == ValueType.NativeFunction):
            result = func.callback(args, env)
            return result
        
        if(func.type == ValueType.Function) :

            fn = cast(FunctionVal, func) 
            scope = Environment(parent=fn.decl_env)

            # create the variables for the parameters list

            assert len(fn.parameters) == len(args)

            for i in range(len(fn.parameters)) :
                # TODO : check the bounds here for args
                # verify arity (no. of arg) of function
                var_name = fn.parameters[i]
                value = args[i]
                scope.decl_var(var_name, value, False)

            result : RuntimeVal = make_null()

            # evaluate the function body line by line
            for stmt in fn.body :
                result = self.evaluate(stmt, scope)

            return result

        print(f'\n[INTERPRETER ERROR] : Cannot call value that is not a function : {func}')
        exit(0)

    def _evaluate_member_expr(self, expr : MemberExpr, env : Environment) -> RuntimeVal :
        
        result = RuntimeVal

        # we do something similar to lodash.get(propery_string)
        # where propery_string is the raw string : "foo.bar.baz"
        # we then handle the lookup on the environment. 
        # we may need to change this in the future maybe ? idk. 
        def extract_value(data):
            if (data.kind == NodeType.MemberExpr):
                obj = extract_value(data.object)
                prop = extract_value(data.property)
                return f'{obj}.{prop}'
            elif (data.kind == NodeType.Identifier):
                return data.symbol
            else:
                print(f'\n[INTERPRETER ERROR] : Error occured while evaluating member expression : {data.to_dict()}')
                exit(0)


        s = extract_value(expr)
        return env.lookup_var(s)

    def _evaluate_variable_decl(self, decl: VariableDecl, env: Environment) -> RuntimeVal:

        val = make_null()

        if (decl.value):
            val = self.evaluate(decl.value, env)
        
        return env.decl_var(var_name=decl.identifier, value=val, constant=decl.constant)

    def _evaluate_function_decl(self, decl : FunctionDecl, env : Environment) -> RuntimeVal :

        # create new function scope
    
        fn = FunctionVal(
            name=decl.name,
            parameters=decl.parameters,
            body=decl.body,
            decl_env=env
        )

        # register the function in the env
        return env.decl_var(decl.name, fn, True)

    def _evaluate_assignment(self, node : AssignmentExpr, env : Environment) -> RuntimeVal :

        if(node.assignee.kind != NodeType.Identifier) :
            print(f'\n[INTERPRETER ERROR] : Invalid LHS inside assignmenr expr : \n{node.assignee.to_dict()}')
            exit(0)
        
        var_name = cast(Identifier, node.assignee).symbol
        value = self.evaluate(node.value, env)
       
        return env.assign_var(var_name, value)

    def _evaluate_program(self, program: Program, env : Environment) -> RuntimeVal :

        last_evaluated: RuntimeVal = make_null()

        for stmt in program.body:
            last_evaluated = self.evaluate(stmt, env)

        return last_evaluated

    def evaluate(self, ast_node: Stmt, env : Environment = None) -> RuntimeVal :

        current_env = env if env is not None else self.global_env

        if (ast_node == None):
            print('f\n[INTERPRETER ERROR] : \AST node is None : {ast_node}')
            exit(0)

        if (ast_node.kind == NodeType.NumericalLiteral):
            return NumberVal(value=ast_node.value)
    
        elif (ast_node.kind == NodeType.BinaryExpr):
            return self._evaluate_binary_expr(ast_node, current_env)
        
        elif(ast_node.kind == NodeType.AssignmentExpr) :
            return self._evaluate_assignment(ast_node, current_env)
    
        elif (ast_node.kind == NodeType.Identifier):
            return self._evaluate_identifier(ast_node, current_env)
            
        elif (ast_node.kind == NodeType.ObjectLiteral):
            return self._evaluate_object_expr(ast_node, current_env)
            
        elif (ast_node.kind == NodeType.CallExpr):
            return self._evaluate_call_expr(ast_node, current_env)
    
        elif (ast_node.kind == NodeType.MemberExpr):
            return self._evaluate_member_expr(ast_node, current_env)
    
        elif (ast_node.kind == NodeType.VariableDecl):
            return self._evaluate_variable_decl(ast_node, current_env)
        
        elif (ast_node.kind == NodeType.FunctionDecl):
            return self._evaluate_function_decl(ast_node, current_env)
    
        elif (ast_node.kind == NodeType.Program):
            return self._evaluate_program(ast_node, current_env)
    
        else:
            print(f'\n[INTERPRETER ERROR] :  This AST node has not been yet been setup for interpretation : \n {ast_node.to_dict()}')
            exit(0)

        
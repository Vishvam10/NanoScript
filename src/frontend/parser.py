from typing import List, cast

from .ast import Stmt, Program, Expr, BinaryExpr, Identifier, NumericLiteral, VariableDecl, AssignmentExpr, PropertyLiteral, ObjectLiteral, CallExpr, MemberExpr, FunctionDecl

from .lexer import TokenType, Token, tokenize

'''
    order of precedence : 

    lower in the tree or the call stack has the highest precedence

    |    Stmt                          (lowest)
    |    Expr | VariableDecl
    |    AssignmentExpr
    |    ObjectExpr
    |    AdditiveExpr
    |    MultiplicativeExpr
    |    CallExpr
    |    MemberExpr
    v    PrimaryExpr                    (highest)

    more precedence = further down the tree

    so, additive calls multiplicative. multiplicative calls primary,
    assignment calls object expression, and so on

    It always passes through the stack. Technically speaking, this 
    would be the grammar of this language at this point :

        Stmt                := Expr | VariableDecl | FunctionDecl
        Expr                := AssignmentExpr
        AssignmentExpr      := AssignmentExpr | ObjectExpr
        ObjectExpr          := Expr | AdditiveExpr
        AdditiveExpr        := MultiplicativeExpr
        MultiplicativeExpr  := PrimaryExpr
'''

class Parser():

    def __init__(self) -> None:
        self._tokens: List[Token] = []
        self._ptr: int = 0

    def _not_eof(self) -> bool:
        return self._tokens[self._ptr].type != TokenType.EOF

    def _at(self) -> Token:
        return self._tokens[self._ptr]

    def _eat(self) -> Token:
        prev = self._at()
        self._ptr += 1
        return prev

    def _expect(self, type: TokenType, err: str):
        prev = self._at()
        if (not prev or prev.type != type):
            print(f'\n[PARSER ERROR] : \n {err}, \n Expected : {type}, \nReceived : ({prev.value}, {prev.type})')
            exit(0)

        self._ptr += 1
        return prev

    def _parse_stmt(self) -> Stmt:

        token_type = self._at().type

        if(token_type == TokenType.Let or token_type == TokenType.Const) :
            return self._parse_variable_decl()
        elif(token_type == TokenType.Fn) :
            return self._parse_function_decl()
        else :
            return self._parse_expr()

    def _parse_variable_decl(self) -> Stmt :
        # 1. let ident;
        # 2. (let | const) ident = Expr;
        is_constant = self._eat().type == TokenType.Const
        identifier = self._expect(
            TokenType.Identifier, 'Expected identifier name following let or const keywords'
        ).value

        token_type = self._at().type

        if(token_type == TokenType.SemiColon) :
            self._eat()  # expect semi-colon
            if(is_constant) :
                print('\n\n[PARSER ERROR] : Must assign value to constant expressions. No value provided')
                exit(0)
            
            return VariableDecl(
                identifier=identifier,
                value=None,
                constant=False  # is_constant is false here anyway
            )
        
        self._expect(
            TokenType.Equals, 
            'Expected equals token following identifier in variable declaration '
        )

        value = self._parse_expr()
        
        self._expect(
            TokenType.SemiColon, 
            'Variable declaration statements must end with semi-colon'
        )

        return VariableDecl(
            identifier=identifier,
            value=value,
            constant=is_constant
        )

    def _parse_function_decl(self) -> Stmt :

        # eat the fn keyword
        self._eat()

        name = self._expect(
            TokenType.Identifier, 
            'Expected function name following fn keyword'
        ).value

        # this also accepts expr but that should not 
        # be allowed in fn decl. so, fn add(x, y) 
        # is allowed but fn add(x + 5, y - 3) is not
        # so we manually check it if it's a string (kinda hacky)
        args = self._parse_args()
        params : List[str] = []

        for arg in args :
            # TOOD : use isinstance() here
            if(isinstance(arg.kind, Identifier)) :
                print(f'\n[PARSER ERROR] : Inside function decl parameters are expected to be of type string : {arg.kind}')
                exit(0)
        
            params.append(cast(Identifier, arg).symbol)

        self._expect(
            TokenType.OpenBrace, 
            'Expected function body following decl'
        )

        body : List[Stmt] = []

        while(
            (self._at().type != TokenType.EOF) and 
            (self._at().type != TokenType.CloseBrace)
        ) :
            stmt = self._parse_stmt()
            body.append(stmt)

        self._expect(
            TokenType.CloseBrace, 
            'Closing brace expected inside function decl'
        )

        return FunctionDecl(
            name=name, 
            parameters=params, 
            body=body
        )


    def _parse_assignment_expr(self) : 
        assignee : Expr = self._parse_object_expr()
        
        token_type : TokenType = self._at().type
        
        if(token_type == TokenType.Equals) :
            self._eat()

            # we do this to allow chaining like a = b = c
            value = self._parse_assignment_expr()
           
            return AssignmentExpr(
                assignee=assignee,
                value=value
            )
        
        return assignee

    def _parse_expr(self) -> Expr:
        return self._parse_assignment_expr()

    def _parse_object_expr(self) -> Expr :

        token_type = self._at().type

        if(token_type != TokenType.OpenBrace) :
            # not an object, so continue
            return self._parse_additive_expr()
        
        # advance past open brace
        self._eat()

        properties : List[PropertyLiteral] = []

        while(self._not_eof() and self._at().type != TokenType.CloseBrace) :

            # we want to handle { key1 : val1, key2 : val2 } AND { key1, key2 }
            
            key = self._expect(
                TokenType.Identifier,
                'Object literal key expected'
            ).value

            token_type = self._at().type

            # allows short hand : { key1, key2 }. so, key : val -> { key }
            if(token_type == TokenType.Comma) :
                # advance past the comma
                self._eat() 

                properties.append(
                    PropertyLiteral(
                        key=key
                    )
                )

                continue

            # allows short hand : { key1, key2 }. so, key : val -> { key }
            elif(token_type == TokenType.CloseBrace) :
                properties.append(
                    PropertyLiteral(
                        key=key
                    )
                )
 
                continue


            # handling { key1 : val1, key2 : val2 } now
            self._expect(
                TokenType.Colon, 
                'Missing colon following identifier in ObjectExpr'
            )

            value = self._parse_expr()

            properties.append(
                PropertyLiteral(
                    key=key,
                    value=value
                )
            )

            if(self._at().type != TokenType.CloseBrace) :
                self._expect(
                    TokenType.Comma,
                    'Expected comma or closing bracket following property'
                )

        self._expect(
            TokenType.CloseBrace, 
            'Object literal missing closing braces'
        )
        
        return ObjectLiteral(
            properties=properties
        )

    def _parse_additive_expr(self) -> Expr:
        # left hand precedence : parse the left expr first
        left = self._parse_multiplicative_expr()

        while (self._at().value == '+' or self._at().value == '-'):
            operator = self._eat().value
            right = self._parse_multiplicative_expr()

            # bubbling it up instead
            left = BinaryExpr(
                left=left,
                right=right,
                operator=operator
            )

        return left

    def _parse_multiplicative_expr(self) -> Expr:

        left = self._parse_call_member_expr()

        while (self._at().value == '/' or self._at().value == '*' or self._at() == '%'):
            operator = self._eat().value
            right = self._parse_call_member_expr()

            # bubbling it up instead
            left = BinaryExpr(
                left=left,
                right=right,
                operator=operator
            )

        return left

    def _parse_call_member_expr(self) -> Expr :
        
        # foo.x() : we want to get rid of foo and x to call it
        member = self._parse_member_expr()

        if(self._at().type == TokenType.OpenParam) :
            return self._parse_call_expr(member)
        
        return member

    def _parse_call_expr(self, caller : Expr) -> Expr :
        
        args = self._parse_args()

        # this takes care of foo.x() or x()
        call_expr = CallExpr(
            args=args,
            caller=caller
        )

        # this allows us do function chaining 
        # something like this : foo.x()() or x()()
        if(self._at().type == TokenType.OpenParam) :
            call_expr = self._parse_call_expr(call_expr)

        return call_expr

    def _parse_args(self) -> List[Expr] :

        # we want to parse things like : add(x + 5, y - 2)
        # by args we mean these not the parameters in 
        # function declaration like : fn add(x, y)

        self._expect(
            TokenType.OpenParam,
            'Expected open parenthesis'
        )

        token_type = self._at().type
        args = []
        
        if(token_type != TokenType.CloseParam) :
            args = self._parse_args_list()

        self._expect(
            TokenType.CloseParam,
            'Expect closing parenthesis inside arguments list'
        )
        
        return args

    def _parse_args_list(self) -> List[Expr] :
        
        # we do this so we could use a while loop and not 
        # something like a do while loop. We parse assignment expr
        # to handle something like this : foo(x = 5, v = "bar")
        args = [self._parse_assignment_expr()]

        while(self._at().type == TokenType.Comma and self._eat()) :
            arg = self._parse_assignment_expr()
            args.append(arg)

        return args

    def _parse_member_expr(self) -> Expr :
        
        obj = self._parse_primary_expr()
        computed = False
        property : Expr = Expr(kind=Expr)

        while(
            (self._at().type == TokenType.Dot) or 
            (self._at().type == TokenType.OpenBracket)    
        ) :
            operator = self._eat()

            # handling non-computed values : foo.bar
            if(operator.type == TokenType.Dot) :
                computed = False
                
                # to get identifier
                property = self._parse_primary_expr()

                if(isinstance(property.kind, Identifier)) :
                    print('\n[PARSER ERROR] : Cannot use dot operator without RHS being an identifier')
            
            else :
                computed = True

                # this allows computed values : foo[computedValue]
                property = self._parse_expr()
                
                self._expect(
                    TokenType.CloseBracket, 
                    'Missing closing bracket in computed value'
                )

                
            obj = MemberExpr(
                object=obj,
                property=property, 
                computed=computed
            )

        return obj

    def _parse_primary_expr(self) -> Expr:

        token_type = self._at().type
        if (token_type == TokenType.Identifier):
            return Identifier(symbol=self._eat().value)

        elif (token_type == TokenType.Number):
            return NumericLiteral(
                value=float(self._eat().value)
            )

        elif (token_type == TokenType.OpenParam):

            # open param
            self._eat()

            value = self._parse_expr()

            # close param, hopefully
            self._expect(
                TokenType.CloseParam, 'Unexpected token found inside parenthesized expression')
            return value

        else:
            print("\nUnexpected token found during parsing : ",
                  self._at().type, self._at().value)
            exit(0)

    def generate_ast(self, src: str) -> Program:
        self._tokens = tokenize(src)
        program: Program = Program()

        while (self._not_eof()):
            program.body.append(
                self._parse_stmt()
            )

        return program

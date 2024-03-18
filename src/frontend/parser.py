from typing import List

from .ast import Stmt, Program, Expr, BinaryExpr, Identifier, NumericLiteral, VariableDecl, AssignmentExpr
from .lexer import TokenType, Token, tokenize

'''
    order of precedence : 
    lower in the tree or the call stack has the highest precedence

    |    AssignmentExpr
    |    AdditiveExpr
    |    MultiplicativeExpr
    v    PrimaryExpr (highest)

    more precedence = further down the tree
    so, additive calls multiplicative. multiplicative calls primary
        
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
            print('[PARSER ERROR] : \n', err,
                  prev.value, ' - Expecting : ', type)
            exit(0)

        self._ptr += 1
        return prev

    def _parse_stmt(self) -> Stmt:

        token_type = self._at().type

        if(token_type == TokenType.Let or token_type == TokenType.Const) :
            return self._parse_variable_decl()
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
                print('[PARSER ERROR] : Must assign value to constant expressions. No value provided')
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

    def _parse_assignment_expr(self) : 
        assignee : Expr = self._parse_additive_expr()
        
        token_type : TokenType = self._at().type
        print()
        print("\nASSIGNEE : ", assignee.to_dict)
        print("\nTOKEN TYPE : ", token_type)
        print()

        if(token_type == TokenType.Equals) :
            print("\nREACHED : ", assignee.to_dict())
            self._eat()
            value = self._parse_assignment_expr
            return AssignmentExpr(
                assignee=assignee,
                value=value
            )
        
        return assignee

    def _parse_expr(self) -> Expr:
        return self._parse_assignment_expr()


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

        left = self._parse_primary_expr()

        while (self._at().value == '/' or self._at().value == '*' or self._at() == '%'):
            operator = self._eat().value
            right = self._parse_primary_expr()

            # bubbling it up instead
            left = BinaryExpr(
                left=left,
                right=right,
                operator=operator
            )

        return left

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
            print("Unexpected token found during parsing : ",
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

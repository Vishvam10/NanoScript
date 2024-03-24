from enum import Enum, auto
from typing import List, Dict

from utils.match import isint, isalpha, isskippable

class TokenType(Enum) :
    Number = auto()
    Identifier = auto()
    

    # ( and )
    OpenParam = auto()
    CloseParam = auto()

    # { and }
    OpenBrace = auto()
    CloseBrace = auto()
    
    # [ and ]
    OpenBracket = auto()
    CloseBracket = auto()
    
    Equals = auto()

    Colon = auto()
    SemiColon = auto()
    Comma = auto()
    Dot = auto()

    BinaryOperator = auto()
    
    Let = auto()
    Const = auto()

    EOF = auto()

KEYWORDS : Dict[str, TokenType] = {
    "let" : TokenType.Let,
    "const" : TokenType.Const
}

class Token() :
    def __init__(self, value : str, type: TokenType) -> None:
        self.value = value
        self.type = type

def tokenize(source) -> List[Token] :

    tokens: List[Token] = []
    src : str = source
    ptr : int = 0

    while(ptr < len(src)) :
        if(src[ptr] == '(') :
            token = Token(src[ptr], TokenType.OpenParam)
            tokens.append(token)
            ptr += 1

        elif(src[ptr] == ')') :
            token = Token(src[ptr], TokenType.CloseParam)
            tokens.append(token)
            ptr += 1
        
        elif(src[ptr] == '{') :
            token = Token(src[ptr], TokenType.OpenBrace)
            tokens.append(token)
            ptr += 1

        elif(src[ptr] == '}') :
            token = Token(src[ptr], TokenType.CloseBrace)
            tokens.append(token)
            ptr += 1
        
        elif(src[ptr] == '[') :
            token = Token(src[ptr], TokenType.OpenBracket)
            tokens.append(token)
            ptr += 1

        elif(src[ptr] == ']') :
            token = Token(src[ptr], TokenType.CloseBracket)
            tokens.append(token)
            ptr += 1
        
        elif(src[ptr] == ':') :
            token = Token(src[ptr], TokenType.Colon)
            tokens.append(token)
            ptr += 1
        
        elif(src[ptr] == ';') :
            token = Token(src[ptr], TokenType.SemiColon)
            tokens.append(token)
            ptr += 1

        elif(src[ptr] == ',') :
            token = Token(src[ptr], TokenType.Comma)
            tokens.append(token)
            ptr += 1

        elif(src[ptr] == '.') :
            token = Token(src[ptr], TokenType.Dot)
            tokens.append(token)
            ptr += 1
        
        elif(src[ptr] in '+-*/%') :
            token = Token(src[ptr], TokenType.BinaryOperator)
            tokens.append(token)
            ptr += 1
        
        elif(src[ptr] == '=') :
            token = Token(src[ptr], TokenType.Equals)
            tokens.append(token)
            ptr += 1



        else :
            # handle mutli-character token (eg. number, let, etc)

            if(isint(src[ptr])) :
                num = ""
                while(ptr < len(src) and isint(src[ptr])) :
                    num += src[ptr]
                    ptr += 1
            
                tokens.append(Token(num, TokenType.Number))
        
            elif(isalpha(src[ptr])) :
                s = ""
                while(ptr < len(src) and isalpha(src[ptr])) :
                    s += src[ptr]
                    ptr += 1
                
                if(s not in KEYWORDS) :
                    tokens.append(Token(s, TokenType.Identifier))
                else :
                    tokens.append(Token(s, KEYWORDS[s]))

            elif(isskippable(src[ptr])) :
                ptr += 1
            
            else :
                print("Unrecognised character found in source : ", src[ptr])
                exit(0)
    
    tokens.append(Token("EOF", TokenType.EOF))
    return tokens

def print_tokens(tokens : List[Token]) -> None :

    for (i, token) in enumerate(tokens) :
        print(f'{i} : ({token.type}, {token.value})')

if __name__ == "__main__" :

    f = open("./tests/lexer.txt", "r")
    source_code = f.read()
    f.close()

    tokens = tokenize(source_code) 
    print_tokens(tokens)
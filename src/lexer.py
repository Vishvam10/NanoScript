from enum import Enum
from typing import List, Dict

from src.match import *

class TokenType(Enum) :
    Number = 0
    Identifier = 1
    Equals = 2
    OpenParam = 3
    CloseParam = 4
    BinaryOperator = 5
    Let = 6

class Token() :
    def __init__(self, value : str, type: TokenType) -> None:
        self.value = value
        self.type = type

KEYWORDS : Dict[str, TokenType] = {
    "let" : TokenType.Let
}

def tokenize(source) :

    tokens: List[Token] = []
    src : str = source
    ptr : int = 0
    print('src : ', src)

    while(ptr < len(src)) :
        if(src[ptr] == '(') :
            token = Token(src[ptr], TokenType.OpenParam)
            tokens.append(token)
            ptr += 1

        elif(src[ptr] == ')') :
            token = Token(src[ptr], TokenType.CloseParam)
            tokens.append(token)
            ptr += 1
        
        elif(src[ptr] in '+-*/') :
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
    
    return tokens

def print_tokens(tokens : List[Token]) :

    for (i, token) in enumerate(tokens) :
        print(f'{i} : ({token.type}, {token.value})')

if __name__ == "__main__" :

    f = open("./tests/lexer.txt", "r")
    source_code = f.read()
    f.close()

    tokens = tokenize(source_code) 
    print_tokens(tokens)
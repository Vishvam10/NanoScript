import re

MATCH_IS_ALPHA = '^[a-zA-Z]+$'
MATCH_IS_INT = '-?\d+(\.\d+)?'

def isalpha(s) :
    return bool(re.match(MATCH_IS_ALPHA, s))

def isint(s) :
    return bool(re.match(MATCH_IS_INT, s))

def isskippable(s) :
    return s == "" or s == " " or s == "\n" or s == "\t"
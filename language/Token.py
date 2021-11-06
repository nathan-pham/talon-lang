ILLEGAL = "ILLEGAL"
EOF = "EOF"

# identifiers and primary data types
IDENT = "IDENT"
INT = "INT"
FLOAT = "FLOAT"
STRING = "STRING"

# operations
ASSIGN = "="
PLUS = "+"
MINUS = "-"
BANG = "!"
ASTERISK = "*"
SLASH = "/"

LT = "<"
GT = ">"
LTE = "<="
GTE = ">="

EQ = "=="
NOT_EQ = "!="

# delimiters
COMMA = ","
COLON = ":"
SEMICOLON = ";"

LPAREN = "("
RPAREN = ")"
LBRACE = "{"
RBRACE = "}"
LBRACKET = "["
RBRACKET = "]"

# keywords
FUNCTION = "FUNCTION"
LET = "LET"
TRUE = "TRUE"
FALSE = "FALSE"
IF = "IF"
ELSE = "ELSE"
RETURN = "RETURN"

def lookup_ident(ident):

    keywords = {
        "function": FUNCTION,
        "let": LET,
        "true": TRUE,
        "false": FALSE,
        "if": IF,
        "else": ELSE,
        "return": RETURN
    }

    return keywords.get(ident, IDENT)

# Token class
class Token:

    # constructor
    def __init__(self, type_, literal):
        self.type_ = type_
        self.literal = literal
    
    # represent token as a str
    def __str__(self):
        return f"<Type: {self.type_}\tLiteral: {self.literal}>"

ILLEGAL = "ILLEGAL"
EOF = "EOF"

# identifiers and literals
IDENT = "IDENT"
INT = "INT"

# operations
ASSIGN = "="
PLUS = "+"
MINUS = "-"
BANG = "!"
ASTERISK = "*"
SLASH = "/"

LT = "<"
GT = ">"

EQ = "=="
NOT_EQ = "!="


# delimiters
COMMA = ","
SEMICOLON = ";"

LPAREN = "("
RPAREN = ")"
LBRACE = "{"
RBRACE = "}"

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
        "fn": FUNCTION,
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

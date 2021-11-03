ILLEGAL = "ILLEGAL"
EOF = "EOF"

# identifiers and literals
IDENT = "IDENT"
INT = "INT"

# operations
ASSIGN = "="
PLUS = "+"

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

def lookup_ident(ident):

    keywords = {
        "fn": FUNCTION,
        "let": LET
    }

    return keywords.get(ident, ident)

# Token class
class Token:

    def __init__(self, type, literal):
        self.type = type
        self.literal = literal
    
    def __str__(self):
        return f"<{self.type} {self.literal}>"
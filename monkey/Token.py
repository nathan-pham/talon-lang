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

# Token class
class Token:

    def __init__(self, type, literal):
        self.type = type
        self.literal = literal
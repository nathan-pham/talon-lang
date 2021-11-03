from monkey.Token import *

def is_letter(char):
    return ("a" <= char and char <= "z") or ("A" <= char and char <= "Z") or char == "_"

def is_digit(char):
    return "0" <= char and char <= "9"

class Lexer:

    input = ""

    char = ""
    position = 0
    read_position = 0
    
    # Lexer constructor
    def __init__(self, input):
        self.input = input
        self.read_char()

    # read character from input
    def read_char(self):

        # read the character; if EOF then set character to 0
        self.char = 0 if self.read_position >= len(self.input) else self.input[self.read_position]

        # save read_position and increment by 1
        self.position = self.read_position
        self.read_position += 1

    # read identifier from input
    def read_identifier(self):

        # cache position
        position = self.position

        # increment position while next token is a letter
        while is_letter(self.char): self.read_char()

        # return identifier
        return self.input[position:self.position]

    # get the next token
    def next_token(self):

        self.skip_whitespace()

        tokens = {
            "=": Token(ASSIGN, self.char),
            ";": Token(SEMICOLON, self.char),
            "(": Token(LPAREN, self.char),
            ")": Token(RPAREN, self.char),
            ",": Token(COMMA, self.char),
            "+": Token(PLUS, self.char),
            "{": Token(LBRACE, self.char),
            "}": Token(RBRACE, self.char),
            0:   Token(EOF, "")
        }

        def default():
            if is_letter(self.char):
                literal = self.read_identifier()
                ident_type = lookup_ident(literal)
                return Token(ident_type, literal)
            else:
                print(self.position)
                return Token(ILLEGAL, self.char)

        token = tokens.get(self.char, default())
        self.read_char()
        return token

    # whitespace is useless
    def skip_whitespace(self):
        while self.char in [" ", "\t", "\n", "\r"]:
            self.read_char()
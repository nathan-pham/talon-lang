from language.Token import *

# Lexer class
class Lexer:

    input_ = ""

    char = ""
    position = 0
    read_position = 0
    
    # constructor
    def __init__(self, input_):
        self.input_ = input_ + "\n" # pad input
        self.read_char()

    # see next character (if any) from input
    def peek_char(self):
        return 0 if self.read_position >= len(self.input_) else self.input_[self.read_position]

    # read character from input
    def read_char(self):

        # read the character, if EOF character -> 0
        self.char = 0 if self.read_position >= len(self.input_) else self.input_[self.read_position]

        # increment read_position
        self.position = self.read_position
        self.read_position += 1

    # read identifier from input
    def read_identifier(self):

        # cache position
        position = self.position

        # increment position while next token is a letter
        while self.char.isalnum() or self.char == "_": self.read_char()
        self.read_position = self.position
        return self.input_[position:self.position]

    # read number from input
    def read_number(self):

        # cache position
        position = self.position

        # increment position while next token is a digit
        while self.char.isnumeric(): self.read_char()
        self.read_position = self.position
        return self.input_[position:self.position]

    # get the next token
    def next_token(self):

        self.skip_whitespace()
        
        token = Token(ILLEGAL, self.char)

        match self.char:

            # double character tokens
            case "=":
                if self.peek_char() == "=":
                    char = self.char
                    self.read_char()             
                    token = Token(EQ, char + self.char)
                else:
                    token = Token(ASSIGN, self.char)
            case "!":
                if self.peek_char() == "=":
                    char = self.char
                    self.read_char()
                    token = Token(NOT_EQ, char + self.char)
                else:
                    token = Token(BANG, self.char)

            # single character tokens
            case ";": token = Token(SEMICOLON, self.char)
            case "(": token = Token(LPAREN, self.char)
            case ")": token = Token(RPAREN, self.char)
            case "{": token = Token(LBRACE, self.char)
            case "}": token = Token(RBRACE, self.char)
            case ",": token = Token(COMMA, self.char)
            case "+": token = Token(PLUS, self.char)
            case "-": token = Token(MINUS, self.char)
            case "*": token = Token(ASTERISK, self.char)
            case "/": token = Token(SLASH, self.char)
            case "<": token = Token(LT, self.char)
            case ">": token = Token(GT, self.char)

            # end of input
            case 0: token = Token(EOF, self.char)

            # identifier or number tokens
            case _:
                if self.char.isalpha() or self.char == "_":
                    literal = self.read_identifier()
                    token = Token(lookup_ident(literal), literal)

                elif self.char.isnumeric():
                    token = Token(INT, self.read_number())

                else:
                    print('hmmm' + self.char)
                    token = Token(ILLEGAL, self.char)

        self.read_char()
        return token

    # whitespace is useless
    def skip_whitespace(self):
        while self.char in [" ", "\t", "\n", "\r"]:
            self.read_char()
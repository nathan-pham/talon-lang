from language.eval.Object import Error
from language.Token import *

# Lexer class
class Lexer:

    input_ = ""

    char = ""
    position = 0
    read_position = 0

    errors = []
    
    # constructor
    def __init__(self, input_):
        self.input_ = input_ # + "\n" # pad input
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
        while self.char != 0 and (self.char.isalnum() or self.char == "_"): self.read_char()
        self.read_position = self.position
        return self.input_[position:self.position]

    # read number from input
    def read_number(self):

        # cache position
        position = self.position

        # increment position while next token is a digit
        while self.char != 0 and (self.char.isnumeric() or self.char == "."): self.read_char()
        self.read_position = self.position
        return self.input_[position:self.position]

    # read string from input
    def read_string(self):
        position = self.position + 1

        while True:
            self.read_char()
            if self.char == '"' or self.char == 0: break

        return self.input_[position:self.position]

    # get the next token
    def next_token(self):

        self.skip_whitespace()
        
        token = Token(ILLEGAL, self.char)

        match self.char:

            # strings
            case '"': token = Token(STRING, self.read_string())

            # comments
            case "#": 
                self.skip_comment()
                return self.next_token()
                
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
            case "<":
                if self.peek_char() == "=":
                    char = self.char
                    self.read_char()
                    token = Token(LTE, char + self.char)
                else:
                    token = Token(LT, self.char)
            case ">":
                if self.peek_char() == "=":
                    char = self.char
                    self.read_char()
                    token = Token(GTE, char + self.char)
                else:
                    token = Token(GT, self.char)

            # single character tokens
            case ":": token = Token(COLON, self.char)
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
            case "[": token = Token(LBRACKET, self.char)
            case "]": token = Token(RBRACKET, self.char)

            # end of input
            case 0: token = Token(EOF, self.char)

            # identifier or number tokens
            case _:
                if self.char.isalpha() or self.char == "_":
                    literal = self.read_identifier()
                    token = Token(lookup_ident(literal), literal)

                elif self.char.isnumeric():
                    number = self.read_number()
                    token = Token(FLOAT if "." in number else INT, number)

                else:
                    self.errors.append(Error(f"Unexpected character {self.char}", "lexer"))
                    token = Token(ILLEGAL, self.char)

        self.read_char()
        return token

    # whitespace is useless
    def skip_whitespace(self):
        while self.char in [" ", "\t", "\n", "\r"]: self.read_char()

    # comments are useless
    def skip_comment(self):
        while not self.char in ["\n", "\r", 0]: self.read_char()
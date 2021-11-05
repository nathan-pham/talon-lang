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

    # see next character (if any) from input
    def peek_char(self):
        return 0 if self.read_position >= len(self.input) else self.input[self.read_position]

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

    # read number from input
    def read_number(self):

        # cache position
        position = self.position

        # increment position while next token is a digit
        while is_digit(self.char): self.read_char()
        
        # return number
        return self.input[position:self.position]

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

            # identifier or number tokens
            case _:
                if is_letter(self.char):
                    literal = self.read_identifier()
                    ident_type = lookup_ident(literal)
                    token = Token(ident_type, literal)

                elif is_digit(self.char):
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
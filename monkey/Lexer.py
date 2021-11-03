import monkey.Token

class Lexer:

    input = ""

    char = ""
    position = 0
    read_position = 0
    
    def __init__(self, input):
        self.input = input

        self.read_char()

    def read_char(self):
        # read the character; if EOF then set character to 0
        self.char = 0 if self.read_position >= len(self.input) else self.input[self.read_position]

        # save read_position and increment by 1
        self.position = self.read_position
        self.read_position += 1

    def next_token(self):

        tokens = {
            "=": Token(ASSIGN, self.char),
            ";": Token(SEMICOLON, self.char),
            "(": Token(LPAREN, self.char),
            ")": Token(RPAREN, self.char),
            ",": Token(COMMA, self.char),
            "+": Token(PLUS, self.char),
            "{": Token(LBRACE, self.char),
            "}": Token(RBRACE, self.char),
            0:   Token(EOF, ""),
        }

        token = tokens.get(self.char, "")
        self.read_char()
        return token
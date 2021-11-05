
from language.Lexer import Lexer
from language.Token import *
from language.ast import *

class Parser:

    current_token = 0
    peek_token = 0
    lexer = None

    errors = []

    def __init__(self, lexer):
        self.lexer = lexer

        self.next_token()
        self.next_token()

    def next_token(self):
        self.current_token = self.peek_token
        self.peek_token = self.lexer.next_token()

    def parse_program(self):
        program = Program()

        while self.current_token.type_ != EOF:
            stmt = self.parse_statement()
            if stmt != None:
                program.statements.append(stmt)
            self.next_token()

        return program

    # parsing methods
    def parse_statement(self):

        if self.current_token.type_ == LET:
            return self.parse_let_statement()

        return None

    def parse_let_statement(self):
        stmt = LetStatement(self.current_token)

        if not self.expect_peek(IDENT):
            return None
        
        stmt.name = Identifier(self.current_token, self.current_token.literal)

        if not self.expect_peek(ASSIGN):
            return None

        # TODO: parse expression, for now just skip to semicolon
        while not self.current_token_is(SEMICOLON):
            self.next_token()

        return stmt

    # assertion methods
    def current_token_is(self, type_):
        return self.current_token.type_ == type_

    def peek_token_is(self, type_):
        return self.peek_token.type_ == type_

    def expect_peek(self, type_):
        if self.peek_token_is(type_):
            self.next_token()
            return True
        else:
            self.peek_error(type_)
            return False

    # error handling
    def peek_error(self, type_):
        self.errors.append(f"expected next token to be {type_}, got {self.peek_token.type_} instead")
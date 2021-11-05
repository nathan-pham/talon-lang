
from language.Lexer import Lexer
from language.Token import *
from language.ast import *

class Parser:

    current_token = 0
    peek_token = 0
    lexer = None

    def __init__(self, lexer):
        self.lexer = lexer

        self.next_token()
        self.next_token()

    def next_token(self):
        self.current_token = self.peek_token
        self.peek_token = self.lexer.next_token()

    def parse_program(self):
        program = Program()

        while self.current_token.type != EOF:
            stmt = self.parse_statement()
            if stmt != None:
                program.statements.append(stmt)
            self.next_token()

        return program

    def parse_statement(self):
        switch = {
            [LET]: self.parse_let_statement()
        }

        return switch.get(self.current_token.type, None)

    def parse_let_statement(self):
        stmt = LetStatement(self.current_token)

        if not self.expect_peek(IDENT):
            return None
        
        stmt.name = Identifier(self.current_token, self.current_token.literal)

        if not self.expect_peek(ASSIGN):
            return None

        while not self.current_token_is(SEMICOLON):
            self.next_token()

        return stmt

    def current_token_is(self, type_):
        return self.current_token.type_ == type_

    def peek_token_is(self, type_):
        return self.peek_token.type_ == type_

    def expect_peek(self, type_):
        if self.peek_token_is(type_):
            self.next_token()
            return True
        else:
            return False

from language.Lexer import Lexer
from language.Token import *
from language.ast import *

# precedence
LOWEST = 0
EQUALS = 1
LESSGREATER = 2
SUM = 3
PRODUCT = 4
PREFIX = 5
CALL = 6

precedences = {
    EQ:         EQUALS,
    NOT_EQ:     EQUALS,
    LT:         LESSGREATER,
    GT:         LESSGREATER,
    PLUS:       SUM,
    MINUS:      SUM,
    SLASH:      PRODUCT,
    ASTERISK:   PRODUCT,
    LPAREN:     CALL
}

# Parser class
class Parser:

    # constructor
    def __init__(self, lexer):
        self.lexer = lexer

        self.current_token = 0
        self.peek_token = 0
        self.next_token()
        self.next_token()

        self.errors = []

        # register prefix and infix
        self.prefix_parse_fns = {}
        self.infix_parse_fns = {}

        self.register_prefix(IDENT, self.parse_identifier)
        self.register_prefix(INT, self.parse_integer_literal)
        self.register_prefix(FLOAT, self.parse_float_literal)
        self.register_prefix(BANG, self.parse_prefix_expression)
        self.register_prefix(MINUS, self.parse_prefix_expression)
        self.register_prefix(TRUE, self.parse_boolean)
        self.register_prefix(FALSE, self.parse_boolean)
        self.register_prefix(LPAREN, self.parse_grouped_expression)
        self.register_prefix(IF, self.parse_if_expression)
        self.register_prefix(FUNCTION, self.parse_function_literal)
        self.register_prefix(STRING, self.parse_string_literal)

        self.register_infix(PLUS, self.parse_infix_expression)
        self.register_infix(MINUS, self.parse_infix_expression)
        self.register_infix(SLASH, self.parse_infix_expression)
        self.register_infix(ASTERISK, self.parse_infix_expression)
        self.register_infix(EQ, self.parse_infix_expression)
        self.register_infix(NOT_EQ, self.parse_infix_expression)
        self.register_infix(LT, self.parse_infix_expression)
        self.register_infix(GT, self.parse_infix_expression)
        self.register_infix(LPAREN, self.parse_call_expression)

    # retrieve the next token
    def next_token(self):
        self.current_token = self.peek_token
        self.peek_token = self.lexer.next_token()

    # register a prefix or infix
    def register_prefix(self, type_, fn):
        self.prefix_parse_fns[type_] = fn

    def register_infix(self, type_, fn):
        self.infix_parse_fns[type_] = fn

    def peek_precedence(self):
        return precedences.get(self.peek_token.type_, LOWEST)

    def current_precedence(self):
        return precedences.get(self.current_token.type_, LOWEST)

    def parse_program(self):
        program = Program()

        while self.current_token.type_ != EOF:
            stmt = self.parse_statement()
            if stmt != None:
                program.statements.append(stmt)
            self.next_token()

        return program
        
    # parse expressions
    def parse_expression(self, precedence):
        prefix = self.prefix_parse_fns.get(self.current_token.type_)
        
        if not prefix:
            self.no_prefix_parse_fn_error(self.current_token.type_)
            return None

        left_expression = prefix()

        while not self.peek_token_is(SEMICOLON) and precedence < self.peek_precedence():
            infix = self.infix_parse_fns.get(self.peek_token.type_)
            if not infix: return left_expression

            self.next_token()
            left_expression = infix(left_expression)

        return left_expression

    def parse_prefix_expression(self):
        expression = PrefixExpression(self.current_token, self.current_token.literal)
        
        self.next_token()
        expression.right = self.parse_expression(PREFIX)
        
        return expression

    def parse_infix_expression(self, left):
        expression = InfixExpression(self.current_token, left, self.current_token.literal)

        precedence = self.current_precedence()
        self.next_token()
        expression.right = self.parse_expression(precedence)

        return expression

    def parse_if_expression(self):
        expression = IfExpression(self.current_token)

        if not self.expect_peek(LPAREN): return None

        self.next_token()
        expression.condition = self.parse_expression(LOWEST)

        if not self.expect_peek(RPAREN): return None
        if not self.expect_peek(LBRACE): return None

        expression.consequence = self.parse_block_statement()

        if self.peek_token_is(ELSE):
            self.next_token()
            if not self.expect_peek(LBRACE): return None
            expression.alternative = self.parse_block_statement()

        return expression

    def parse_grouped_expression(self):
        self.next_token()

        expression = self.parse_expression(LOWEST)
        if not self.expect_peek(RPAREN):
            return None

        return expression
    
    def parse_call_expression(self, function):
        expression = CallExpression(self.current_token, function)
        expression.arguments = self.parse_call_arguments()

        return expression

    def parse_call_arguments(self):
        arguments = []

        if self.peek_token_is(RPAREN):
            self.next_token()
            return arguments

        self.next_token()
        arguments.append(self.parse_expression(LOWEST))

        while self.peek_token_is(COMMA):
            self.next_token()
            self.next_token()
            arguments.append(self.parse_expression(LOWEST))
            
        if not self.expect_peek(RPAREN): return None
        return arguments

    # parse literals
    def parse_identifier(self):
        return Identifier(self.current_token, self.current_token.literal)

    def parse_integer_literal(self):
        try: 
            literal = IntegerLiteral(self.current_token, int(self.current_token.literal))
            return literal
        except ValueError:
            self.errors.append(f"could not parse {self.current_token.literal} as an integer")
            return None

    def parse_float_literal(self):
        try:
            literal = FloatLiteral(self.current_token, float(self.current_token.literal))
            return literal
        except ValueError:
            self.errors.append(f"could not parse {self.current_token.literal} as a float")
            return None

    def parse_boolean(self):
        return Boolean(self.current_token, self.current_token_is(TRUE))

    def parse_function_literal(self):
        literal = FunctionLiteral(self.current_token)

        if not self.expect_peek(LPAREN): return None
        literal.parameters = self.parse_function_parameters()

        if not self.expect_peek(LBRACE): return None
        literal.body = self.parse_block_statement()

        return literal

    def parse_function_parameters(self):
        identifiers = []

        if self.peek_token_is(RPAREN):
            self.next_token()
            return identifiers

        self.next_token()

        identifier = Identifier(self.current_token, self.current_token.literal)
        identifiers.append(identifier)

        while self.peek_token_is(COMMA):
            self.next_token()
            self.next_token()
            identifier = Identifier(self.current_token, self.current_token.literal)
            identifiers.append(identifier)

        if not self.expect_peek(RPAREN): return None
        return identifiers

    def parse_string_literal(self):
        return StringLiteral(self.current_token, self.current_token.literal)
    
    # parse statements
    def parse_statement(self):

        if self.current_token.type_ == LET:
            return self.parse_let_statement()
        elif self.current_token.type_ == RETURN:
            return self.parse_return_statement()

        return self.parse_expression_statement()

    def parse_let_statement(self):
        stmt = LetStatement(self.current_token)

        if not self.expect_peek(IDENT):
            return None
        
        stmt.name = Identifier(self.current_token, self.current_token.literal)

        if not self.expect_peek(ASSIGN):
            return None

        self.next_token()

        stmt.value = self.parse_expression(LOWEST)
        if self.peek_token_is(SEMICOLON): self.next_token()

        return stmt
    
    def parse_return_statement(self):
        stmt = ReturnStatement(self.current_token)

        self.next_token()

        stmt.return_value = self.parse_expression(LOWEST)
        if self.peek_token_is(SEMICOLON): self.next_token()

        return stmt

    def parse_expression_statement(self):
        stmt = ExpressionStatement(self.current_token, self.parse_expression(LOWEST))

        if self.peek_token_is(SEMICOLON):
            self.next_token()

        return stmt

    def parse_block_statement(self):
        block = BlockStatement(self.current_token)

        self.next_token()

        while not self.current_token_is(RBRACE) and not self.current_token_is(EOF):
            stmt = self.parse_statement()
            if stmt != None:
                block.statements.append(stmt)
            self.next_token()
        
        return block

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

    def no_prefix_parse_fn_error(self, type_):
        self.errors.append(f"no prefix parse function for {type_} found")
class Node:
    def token_literal(self):
        pass

class Statement(Node):
    def statement_node(self):
        pass

class Expression(Node):
    def expression_node(self):
        pass

class Program:

    statements = []

    def token_literal(self):
        if len(self.statements) > 0:
            return self.statements[0].token_literal()
        else:
            return None

class LetStatement:
    def __init__(self, token, name, value):
        self.token = token
        self.name = name
        self.value = value

    def statement_node(self):
        pass

    def token_literal(self):
        return self.token.literal

class Identifier:
    def __init__(self, token, value):
        self.token = token
        self.value = value

    def expression_node(self):
        pass

    def token_literal(self):
        return self.token.literal
# Talon Program class
class Program:

    statements = []

    def token_literal(self):
        if len(self.statements) > 0:
            return self.statements[0].token_literal()
        else:
            return None

# Node class
class Node:
    def token_literal(self):
        return self.token.literal

    def __str__(self):
        return self.token_literal()

# Node -> Statement class
class Statement(Node):
    def statement_node(self):
        pass

# Node -> Expression class
class Expression(Node):
    value = None
    token = None

    def expression_node(self):
        pass

    def __str__(self):
        return self.token_literal()

# Node -> Statement -> ExpressionStatement class
class ExpressionStatement(Statement):
    def __init__(self, token, expression=None):
        self.token = token
        self.expression = expression

# Node -> Statement -> ReturnStatement class
class ReturnStatement(Statement):
    def __init__(self, token, return_value=None):
        self.token = token
        self.return_value = return_value

# Node -> Statement -> LetStatement class
class LetStatement(Statement):
    def __init__(self, token, name=None, value=None):
        self.token = token
        self.name = name
        self.value = value

    def statement_node(self):
        pass

# Node -> Expression -> Identifier class
class Identifier(Expression):
    def __init__(self, token, value):
        self.token = token
        self.value = value

# Node -> Expression -> IntegerLiteral class
class IntegerLiteral(Expression):
    token = None
    value = None

    def __init__(self, token, value=None):
        self.token = token
        self.value = value
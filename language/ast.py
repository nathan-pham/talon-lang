# Talon Program class
class Program:

    def __init__(self):
        self.statements = []

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
    token = None

    def statement_node(self):
        pass

# Node -> Expression class
class Expression(Node):
    token = None
    value = None

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

# Node -> Statement -> BlockStatement class
class BlockStatement(Statement):
    def __init__(self, token):
        self.token = token
        self.statements = []

# Node -> Expression -> Identifier class
class Identifier(Expression):
    def __init__(self, token, value):
        self.token = token
        self.value = value

# Node -> Expression -> IntegerLiteral class
class IntegerLiteral(Expression):
    def __init__(self, token, value=None):
        self.token = token
        self.value = value

# Node -> Expression -> Boolean class
class Boolean(Expression):
    def __init__(self, token, value=None):
        self.token = token
        self.value = value

# Node -> Expression -> PrefixExpression class
class PrefixExpression(Expression):
    def __init__(self, token, operator, right=None):
        self.token = token
        self.operator = operator
        self.right = right

# Node -> Expression -> InfixExpression class
class InfixExpression(Expression):
    def __init__(self, token, left, operator, right=None):
        self.token = token
        self.left = left
        self.operator = operator
        self.right = right

# Node -> Expression -> IfExpression class
class IfExpression(Expression):
    def __init__(self, token, condition=None, consequence=None, alternative=None):
        self.token = token
        self.condition = condition
        self.consequence = consequence
        self.alternative = alternative

# Node -> Expression -> FunctionLiteral class
class FunctionLiteral(Expression):
    def __init__(self, token, body=None):
        self.token = token
        self.parameters = []
        self.body = body
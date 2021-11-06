import language.eval.Object as Object
from language.ast import *

TRUE = Object.Boolean(True)
FALSE = Object.Boolean(False)
NULL = Object.Null()

def eval(node):
    if isinstance(node, Program): return eval_statements(node.statements)
    elif isinstance(node, ExpressionStatement): return eval(node.expression)
    elif isinstance(node, IntegerLiteral): return Object.Integer(node.value)
    elif isinstance(node, Boolean): return TRUE if node.value else FALSE
    elif isinstance(node, PrefixExpression): 
        right = eval(node.right)
        return eval_prefix_expression(node.operator, right)

    elif isinstance(node, InfixExpression):
        left = eval(node.left)
        right = eval(node.right)
        return eval_infix_expression(node.operator, left, right)

def eval_statements(stmts):
    result = None
    for stmt in stmts: result = eval(stmt)
    return result

def eval_prefix_expression(operator, right):
    match operator:
        case "!": return eval_bang_operator_expression(right)
        case "-": return eval_minus_prefix_expression(right)
        case _: return NULL

def eval_bang_operator_expression(right):
    # from utils.JSON import JSON
    # print(JSON.serialize(right))
    if isinstance(right, Object.Boolean): return FALSE if right.value else TRUE
    elif isinstance(right, Object.Null): return TRUE
    else: return FALSE

def eval_minus_prefix_expression(right):
    if right.type_ != Object.INTEGER_OBJ: return NULL
    return Object.Integer(-1 * right.value)

def eval_infix_expression(operator, left, right):
    if isinstance(left, Object.Integer) and isinstance(right, Object.Integer):
        return eval_integer_infix_expression(operator, left, right)
    else: return NULL

def eval_integer_infix_expression(operator, left, right):
    match operator:
        case "+":
            return Object.Integer(left.value + right.value)
        case "-":
            return Object.Integer(left.value - right.value)
        case "*":
            return Object.Integer(left.value * right.value)
        case "/":
            return Object.Integer(left.value / right.value)
        case _:
            return NULL
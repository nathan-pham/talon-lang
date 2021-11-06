import language.eval.Object as Object
from language.ast import *

TRUE = Object.Boolean(True)
FALSE = Object.Boolean(False)
NULL = Object.Null()

def native_bool_to_boolean_object(value):
    if value:
        return TRUE
    else:
        return FALSE

def is_truthy(obj):
    if obj == NULL: return False
    elif obj == TRUE: return True
    elif obj == FALSE: return False
    else: return True

def eval(node):
    if isinstance(node, Program): return eval_statements(node.statements)
    elif isinstance(node, ExpressionStatement): return eval(node.expression)
    elif isinstance(node, IntegerLiteral): return Object.Integer(node.value)
    elif isinstance(node, Boolean): return native_bool_to_boolean_object(node.value)
    elif isinstance(node, PrefixExpression): 
        right = eval(node.right)
        return eval_prefix_expression(node.operator, right)
    elif isinstance(node, InfixExpression):
        left = eval(node.left)
        right = eval(node.right)
        return eval_infix_expression(node.operator, left, right)
    elif isinstance(node, BlockStatement): return eval_statements(node.statements)
    elif isinstance(node, IfExpression): return eval_if_expression(node)

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
    elif operator == "==": return native_bool_to_boolean_object(left == right)
    elif operator == "!=": return native_bool_to_boolean_object(left != right)
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
        case "<":
            return native_bool_to_boolean_object(left.value < right.value)
        case ">":
            return native_bool_to_boolean_object(left.value > right.value)
        case "==":
            return native_bool_to_boolean_object(left.value == right.value)
        case "!=":
            return native_bool_to_boolean_object(left.value != right.value)
        case _:
            return NULL

def eval_if_expression(ie):
    condition = eval(ie.condition)

    if is_truthy(condition): return eval(ie.consequence)
    elif ie.alternative != None: return eval(ie.alternative)
    else: return NULL
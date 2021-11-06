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
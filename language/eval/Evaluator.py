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

def eval_statements(stmts):
    result = None
    for stmt in stmts: result = eval(stmt)
    return result
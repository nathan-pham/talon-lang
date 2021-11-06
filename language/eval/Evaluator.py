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

def is_error(obj):
    return obj and obj.type_ == Object.ERROR_OBJ

def eval(node, env):
    if isinstance(node, Program): return eval_program(node, env)
    elif isinstance(node, ExpressionStatement): return eval(node.expression, env)
    elif isinstance(node, IntegerLiteral): return Object.Integer(node.value)
    elif isinstance(node, Boolean): return native_bool_to_boolean_object(node.value)

    elif isinstance(node, PrefixExpression): 
        right = eval(node.right, env)
        if is_error(right): return right
        return eval_prefix_expression(node.operator, right)
    elif isinstance(node, InfixExpression):
        left = eval(node.left, env)
        right = eval(node.right, env)
        if is_error(left): return left
        if is_error(right): return right
        return eval_infix_expression(node.operator, left, right)

    elif isinstance(node, BlockStatement): return eval_block_statement(node, env)
    elif isinstance(node, IfExpression): return eval_if_expression(node, env)

    elif isinstance(node, ReturnStatement):
        value = eval(node.return_value, env)
        if is_error(value): return value
        return Object.ReturnValue(value)

    elif isinstance(node, LetStatement):
        value = eval(node.value, env)
        if is_error(value): return value

def eval_program(program, env):
    result = None

    for stmt in program.statements:
        result = eval(stmt, env)
        if isinstance(result, Object.ReturnValue): return result.value
        elif isinstance(result, Object.Error): return result

    return result

def eval_block_statement(block, env):
    result = None

    for stmt in block.statements:
        result = eval(stmt, env)
        if result and (result.type_ == Object.RETURN_VALUE_OBJ or result.type_ == Object.ERROR_OBJ): return result

    return result

def eval_statements(stmts, env):
    result = None

    for stmt in stmts: 
        result = eval(stmt, env)
        if isinstance(result, Object.ReturnValue): return result.value

    return result

def eval_prefix_expression(operator, right):
    match operator:
        case "!": return eval_bang_operator_expression(right)
        case "-": return eval_minus_prefix_expression(right)
        case _: return Object.Error(f"unknown operator: {operator} {right.type_}")

def eval_bang_operator_expression(right):
    # from utils.JSON import JSON
    # print(JSON.serialize(right))
    if isinstance(right, Object.Boolean): return FALSE if right.value else TRUE
    elif isinstance(right, Object.Null): return TRUE
    else: return FALSE

def eval_minus_prefix_expression(right):
    if right.type_ != Object.INTEGER_OBJ: return Object.Error(f"unknown operator: -{right.type_}")
    return Object.Integer(-1 * right.value)

def eval_infix_expression(operator, left, right):
    if isinstance(left, Object.Integer) and isinstance(right, Object.Integer):
        return eval_integer_infix_expression(operator, left, right)
    elif operator == "==": return native_bool_to_boolean_object(left == right)
    elif operator == "!=": return native_bool_to_boolean_object(left != right)
    elif left.type_ != right.type_: return Object.Error(f"type mismatch: {left.type_} {operator} {right.type_}")
    else: return Object.Error(f"unknown operator: {left.type_} {operator} {right.type_}")

def eval_integer_infix_expression(operator, left, right):
    match operator:
        case "+": return Object.Integer(left.value + right.value)
        case "-": return Object.Integer(left.value - right.value)
        case "*": return Object.Integer(left.value * right.value)
        case "/": return Object.Integer(left.value / right.value)
        case "<": return native_bool_to_boolean_object(left.value < right.value)
        case ">": return native_bool_to_boolean_object(left.value > right.value)
        case "==": return native_bool_to_boolean_object(left.value == right.value)
        case "!=": return native_bool_to_boolean_object(left.value != right.value)
        case _: return NULL

def eval_if_expression(ie, env):
    condition = eval(ie.condition, env)

    if is_error(condition): return condition

    if is_truthy(condition): return eval(ie.consequence, env)
    elif ie.alternative != None: return eval(ie.alternative, env)
    else: return NULL
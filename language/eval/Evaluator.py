
from language.eval.native import native_functions
from language.Token import *
from language.ast import *

from utils.JSON import JSON

from language.eval.Environment import Environment
import language.eval.Object as Object

from language.Lexer import Lexer
from language.Parser import Parser


TRUE = Object.Boolean(True)
FALSE = Object.Boolean(False)
NULL = Object.Null()

def native_bool_to_boolean_object(value):
    return TRUE if value else FALSE

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
    elif isinstance(node, IntegerLiteral): return Object.Number(int(node.value))
    elif isinstance(node, FloatLiteral): return Object.Number(float(node.value))
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
        if env.get(node.name.value): return Object.Error(f"identifier '{node.name.value}' already declared")
        env.set(node.name.value, value)
    elif isinstance(node, AssignmentStatement):
        value = eval(node.value, env)
        if is_error(value): return value

        if not env.get(node.name.value): return Object.Error(f"identifier '{node.name.value}' not declared")
        env.set(node.name.value, value)
    
    elif isinstance(node, ImportStatement):
        with open(f"{node.file}.talon", "r") as file:
            file_contents = file.read().strip()
            file_env = talon_lang(file_contents, Environment(), False)

            for key, value in file_env.store.items():
                env.set(key, value)
        
    elif isinstance(node, Identifier): return eval_identifier(node, env)

    elif isinstance(node, FunctionLiteral): return Object.Function(node.parameters, node.body, env)
    elif isinstance(node, CallExpression):
        function = eval(node.function, env)
        if is_error(function): return function

        arguments = eval_expressions(node.arguments, env)
        if len(arguments) == 1 and is_error(arguments[0]): return arguments[0]

        return apply_function(function, arguments)

    elif isinstance(node, StringLiteral): return Object.String(node.value)

    elif isinstance(node, ArrayLiteral):
        elements = eval_expressions(node.elements, env)
        if len(elements) == 1 and is_error(elements[0]): return elements[0]
        return Object.Array(elements)
    elif isinstance(node, IndexExpression):
        left = eval(node.left, env)
        if is_error(left): return left

        index = eval(node.index, env)
        if is_error(index): return index

        return eval_index_expression(left, index)

    elif isinstance(node, DotExpression):
        function = eval(node.function, env)
        if is_error(function): return function

        arguments = eval_expressions(node.arguments, env)
        if len(arguments) == 1 and is_error(arguments[0]): return arguments[0]

        return apply_function(function, arguments)
    
    elif isinstance(node, HashLiteral):
        pairs = {}

        for key, value in node.pairs.items():
            key_obj = eval(key, env)
            if is_error(key_obj): return key_obj
            if not key_obj.hashable(): return Object.Error(f"unusable as hash key: {key_obj.type_}")

            value_obj = eval(value, env)
            if is_error(value_obj): return value_obj

            pairs[key_obj.hash_key()] = Object.HashPair(key_obj, value_obj)

        return Object.Hash(pairs)

def eval_program(program, env):
    result = None

    for stmt in program.statements:
        result = eval(stmt, env)
        if isinstance(result, Object.ReturnValue): return result.value
        elif isinstance(result, Object.Error): return result

    return result

def eval_statements(stmts, env):
    result = None

    for stmt in stmts: 
        result = eval(stmt, env)
        if isinstance(result, Object.ReturnValue): return result.value

    return result

def eval_block_statement(block, env):
    result = None

    for stmt in block.statements:
        result = eval(stmt, env)
        if result and (result.type_ == Object.RETURN_VALUE_OBJ or result.type_ == Object.ERROR_OBJ): return result

    return result

def eval_expressions(expressions, env):
    result = []

    for expr in expressions:
        evaluated = eval(expr, env)
        if is_error(evaluated): return [evaluated]
        result.append(evaluated)

    return result

def eval_prefix_expression(operator, right):
    match operator:
        case "!": return eval_bang_operator_expression(right)
        case "-": return eval_minus_prefix_expression(right)
        case _: return Object.Error(f"unknown operator: {operator} {right.type_}")

def eval_bang_operator_expression(right):
    if isinstance(right, Object.Boolean): return FALSE if right.value else TRUE
    elif isinstance(right, Object.Null): return TRUE
    else: return FALSE

def eval_minus_prefix_expression(right):
    if right.type_ != Object.NUMBER_OBJ: return Object.Error(f"unknown operator: -{right.type_}")
    return Object.Number(-1 * right.value)

def eval_infix_expression(operator, left, right):
    if isinstance(left, Object.Number) and isinstance(right, Object.Number):
        return eval_number_infix_expression(operator, left, right)

    elif operator == "==": return native_bool_to_boolean_object(left == right)
    elif operator == "!=": return native_bool_to_boolean_object(left != right)

    elif left.type_ == Object.STRING_OBJ and right.type_ == Object.STRING_OBJ:
        return eval_string_infix_expression(operator, left, right)

    elif left.type_ != right.type_: return Object.Error(f"type mismatch: {left.type_} {operator} {right.type_}")
    else: return Object.Error(f"unknown operator: {left.type_} {operator} {right.type_}")

def eval_number_infix_expression(operator, left, right):
    match operator:
        case "+": return Object.Number(left.value + right.value)
        case "-": return Object.Number(left.value - right.value)
        case "*": return Object.Number(left.value * right.value)
        case "/": return Object.Number(left.value / right.value)
        case "<": return native_bool_to_boolean_object(left.value < right.value)
        case ">": return native_bool_to_boolean_object(left.value > right.value)
        case "<=": return native_bool_to_boolean_object(left.value <= right.value)
        case ">=": return native_bool_to_boolean_object(left.value >= right.value)
        case "==": return native_bool_to_boolean_object(left.value == right.value)
        case "!=": return native_bool_to_boolean_object(left.value != right.value)
        case _: return NULL

def eval_string_infix_expression(operator, left, right):
    if operator != "+": return Object.Error(f"unknown operator: {left.type_} {operator} {right.type_}")
    return Object.String(left.value + right.value)

def eval_if_expression(ie, env):
    condition = eval(ie.condition, env)

    if is_error(condition): return condition

    if is_truthy(condition): return eval(ie.consequence, env)
    elif ie.alternative != None: return eval(ie.alternative, env)
    else: return NULL

def eval_identifier(node, env):
    val = env.get(node.value)
    if val: return val

    native_fn = native_functions.get(node.value)
    if native_fn: return native_fn

    if node.prototype:
        prototype = eval(node.prototype, env)
    
        if hasattr(prototype, node.value):
            return Object.Native(getattr(prototype, node.value))
        return Object.Error(f"identifier not found: {node.value}")
        # print(JSON.serialize(prototype))
        # prototype_fn = (prototype_functions.get(.token.type_) or {}).get(node.value)
        # return prototype_fn(node.prototype) if prototype_fn else 

    return Object.Error(f"identifier not found: {node.value}")

def apply_function(function, arguments):
    if isinstance(function, Object.Function): 
        extendedEnv = extend_function_env(function, arguments)
        if isinstance(extendedEnv, Object.Error): return extendedEnv

        evaluated = eval(function.body, extendedEnv)
        return evaluated.value if isinstance(evaluated, Object.ReturnValue) else evaluated 
        
        # Object.Error("function {function.body} not declared")

    elif isinstance(function, Object.Native): return function.function(*arguments)

    return Object.Error(f"not a function: {function.type_}")

def extend_function_env(function, arguments):
    env = function.env.extend()

    if len(function.parameters) != len(arguments): 
        return Object.Error(f"wrong number of arguments: {len(function.parameters)} required but {len(arguments)} given")

    for i in range(len(function.parameters)): env.set(function.parameters[i].value, arguments[i])
    return env

def eval_index_expression(left, index):
    if left.type_ == Object.ARRAY_OBJ and isinstance(index, Object.Number):
        return eval_array_index_expression(left, index)
    elif left.type_ == Object.HASH_OBJ:
        return eval_hash_index_expression(left, index)
    elif left.type_ == Object.STRING_OBJ:
        return Object.String(left.value[index.value])
    else: return Object.Error(f"index operator not supported: {left.type_}")

def eval_array_index_expression(left, index):
    idx = index.value
    if idx < 0 or idx >= len(left.elements): return NULL
    return left.elements[idx]

def eval_hash_index_expression(left, index):
    if not index.hashable(): return Object.Error(f"unusable as hash key: {hash.type_}")

    for key, value in left.pairs.items():
        if key.value == index.value and key.type_ == index.type_: return value.value

    return NULL

def talon_lang(input_, environment, inspect=True):
    lexer = Lexer(input_)
    parser = Parser(lexer)
    program = parser.parse_program()

    errors = lexer.errors + parser.errors
    for error in errors: print(error.inspect())

    if len(errors) == 0:
        evaluated = eval(program, environment)
        if evaluated and inspect: print(evaluated.inspect())
        elif isinstance(evaluated, Object.Error): print(evaluated.inspect())

    return environment
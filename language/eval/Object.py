# object types
from language.Token import FLOAT

INTEGER_OBJ = "INTEGER"
FLOAT_OBJ = "FLOAT"
NUMBER_OBJ = "NUMBER" # (INTEGER_OBJ, FLOAT_OBJ)

BOOLEAN_OBJ = "BOOLEAN"
NULL_OBJ = "NULL"

RETURN_VALUE_OBJ = "RETURN_VALUE"
FUNCTION_OBJ = "FUNCTION"
STRING_OBJ = "STRING"
ARRAY_OBJ = "ARRAY"

ERROR_OBJ = "ERROR"

NATIVE_OBJ = "NATIVE"

# Object class
class Object:
    def __init__(self):
        self.type_ = None

    def inspect(self):
        pass

# Object -> Integer class
# class Integer(Object):
#     def __init__(self, value):
#         self.value = int(value)
#         self.type_ = NUMBER_OBJ

#     def inspect(self):
#         return self.value

# Object -> Float class
# class Float(Object):
#     def __init__(self, value):
#         self.value = float(value)
#         self.type_ = NUMBER_OBJ

#     def inspect(self):
#         return self.value

# Object -> Number class:
class Number(Object):
    def __init__(self, value):
        self.value = value
        self.type_ = NUMBER_OBJ

    def inspect(self):
        return self.value

# Object -> Boolean class
class Boolean(Object):
    def __init__(self, value):
        self.value = value
        self.type_ = BOOLEAN_OBJ

    def inspect(self):
        return str(self.value).lower()

# Object -> Null class
class Null(Object):
    def __init__(self):
        self.type_ = NULL_OBJ

    def inspect(self):
        return "null"

# Object -> ReturnValue class
class ReturnValue(Object):
    def __init__(self, value):
        self.value = value
        self.type_ = RETURN_VALUE_OBJ

    def inspect(self):
        return self.value.inspect()

# Object -> Error class
class Error(Object):
    def __init__(self, message):
        self.message = message
        self.type_ = ERROR_OBJ

    def inspect(self):
        return f"ERROR: {self.message}"

# Object -> Function class
class Function(Object):
    def __init__(self, parameters, body, env):
        self.parameters = parameters
        self.body = body
        self.env = env
        self.type_ = FUNCTION_OBJ

    def inspect(self):
        _parameters = ", ".join([p.value for p in self.parameters])

        # TODO: self.body -> actual statements, edit ast.py
        return f"fn({_parameters}) {{\n ... \n}}"

# Object -> String class
class String(Object):
    def __init__(self, value):
        self.value = value
        self.type_ = STRING_OBJ

    def inspect(self):
        return f'"{self.value}"'

# Object -> Native class
class Native(Object):
    def __init__(self, function):
        self.function = function
        self.type_ = NATIVE_OBJ

    def inspect(self):
        return f"[NATIVE_CODE]"

# Object -> Array class
class Array(Object):
    def __init__(self, elements):
        self.elements = elements
        self.type_ = ARRAY_OBJ

    def inspect(self):
        _elements = ", ".join([str(e.inspect()) for e in self.elements])
        return f"[{_elements}]"
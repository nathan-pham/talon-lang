# object types
INTEGER_OBJ = "INTEGER"
FLOAT_OBJ = "FLOAT"
NUMBER_OBJ = "NUMBER" # (INTEGER_OBJ, FLOAT_OBJ)

BOOLEAN_OBJ = "BOOLEAN"
NULL_OBJ = "NULL"

RETURN_VALUE_OBJ = "RETURN_VALUE"
FUNCTION_OBJ = "FUNCTION"
STRING_OBJ = "STRING"
ARRAY_OBJ = "ARRAY"
HASH_OBJ = "HASH"

NATIVE_OBJ = "NATIVE"
ERROR_OBJ = "ERROR"

# Object class
class Object:
    def __init__(self):
        self.type_ = None

    def inspect(self):
        pass

    def hashable(self):
        return hasattr(self, "hash_key") and callable(self.hash_key)

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
    
    def hash_key(self):
        return HashKey(self.type_, self.value)

# Object -> Boolean class
class Boolean(Object):
    def __init__(self, value):
        self.value = value
        self.type_ = BOOLEAN_OBJ

    def inspect(self):
        return str(self.value).lower()

    def hash_key(self):
        value = 1 if self.value else 0
        return HashKey(self.type_, value)

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
    def __init__(self, message, where="Interpreter"):
        self.message = message
        self.type_ = ERROR_OBJ
        self.where = where.upper()

    def inspect(self):
        return f"\033[91m{self.where} ERROR\t{self.message}\x1b[0m"

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

    def hash_key(self):
        return HashKey(self.type_, self.value)

    def ok(self, *args):
        return "ok!"

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

    def append(self, value):
        self.elements.append(value)
        return self

# Object -> HashKey class
class HashKey(Object):
    def __init__(self, type_, value):
        self.type_ = type_
        self.value = value

    def inspect(self):
        if self.type_ == BOOLEAN_OBJ: return "true" if self.value else "false"
        return self.value

# Object -> HashPair class
class HashPair(Object):
    def __init__(self, key, value):
        self.key = key
        self.value = value

    def inspect(self):
        return self.value.inspect()

# Object -> Hash class
class Hash(Object):
    def __init__(self, pairs):
        self.pairs = pairs or {}
        self.type_ = HASH_OBJ

    def inspect(self):
        _pairs = ", ".join([f"{k.inspect()}: {v.inspect()}" for k, v in self.pairs.items()])
        return f"{{{_pairs}}}"
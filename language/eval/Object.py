# data types
INTEGER_OBJ = "INTEGER"
BOOLEAN_OBJ = "BOOLEAN"
NULL_OBJ = "NULL"

# Object class
class Object:
    def __init__(self):
        self.type_ = None

    def inspect(self):
        pass

# Object -> Integer class
class Integer(Object):
    def __init__(self, value):
        self.value = int(value)
        self.type_ = INTEGER_OBJ

    def inspect(self):
        return self.value

# Object -> Boolean class
class Boolean(Object):
    def __init__(self, value):
        self.value = value
        self.type_ = BOOLEAN_OBJ

    def inspect(self):
        return self.value

# Object -> Null class
class Null(Object):
    def __init__(self):
        self.type_ = NULL_OBJ

    def inspect(self):
        return "null"
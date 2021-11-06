import language.eval.Object as Object

TRUE = Object.Boolean(True)
FALSE = Object.Boolean(False)
NULL = Object.Null()

def len_(*args):
    error = argument_error(args, 1)
    if error: return error

    if isinstance(args[0], Object.String): return Object.Number(len(args[0].value))
    if isinstance(args[0], Object.Array): return Object.Number(len(args[0].elements))

    return Object.Error(f"argument to 'len' not supported, got: {args[0].type_}")

def print_(*args):
    for arg in args: print(arg.inspect())
    return NULL

def str_(*args):
    error = argument_error(args, 1)
    if error: return error

    return Object.String(str(args[0]))

def int_(*args):
    error = argument_error(args, 1)
    if error: return error

    if isinstance(args[0], Object.Number): return Object.Number(int(args[0].value))
    if isinstance(args[0], Object.String): return Object.Number(int(args[0].value))

    return Object.Error(f"argument to 'int' not supported, got: {args[0].type_}")

def float_(*args):
    error = argument_error(args, 1)
    if error: return error

    if isinstance(args[0], Object.Number): return Object.Number(float(args[0].value))
    if isinstance(args[0], Object.String): return Object.Number(float(args[0].value))

    return Object.Error(f"argument to 'float' not supported, got: {args[0].type_}")

def type_(*args):
    error = argument_error(args, 1)
    if error: return error

    return Object.String(args[0].type_)

def argument_error(args, required):
    if len(args) != required:
        return Object.Error(f"wrong number of arguments: {required} required but {len(args)} given")

native_functions = {
    # length of objects
    "len": Object.Native(len_),

    # output to display
    "print": Object.Native(print_),

    # loose type checking
    "str": Object.Native(str_),
    "int": Object.Native(int_),
    "float": Object.Native(float_),
    "type": Object.Native(type_),
}
import language.eval.Object as Object

def len_(*args):
    if len(args) != 1: return Object.Error(f"wrong number of arguments: 1 required but {len(args)} given") 

    if isinstance(args[0], Object.String): return Object.Number(len(args[0].value))
    if isinstance(args[0], Object.Array): return Object.Number(len(args[0].elements))

    return Object.Error(f"argument to 'len' not supported, got: {args[0].type_}")

native_functions = {
    "len": Object.Native(len_)
}
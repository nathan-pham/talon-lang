from language.Lexer import Lexer
from language.Parser import Parser

from language.eval.Environment import Environment
from language.eval.evaluator import eval

from utils.JSON import JSON

import platform

pkg_name = "TalonLang"
version = "0.0.1"

def read_file(path):
    with open(path, "r") as file:
        file_contents = file.read().strip()
        
        lexer = Lexer(file_contents)
        parser = Parser(lexer)
        program = parser.parse_program()
        # for statement in program.statements:
        print(JSON.serialize(program.statements))
        print(parser.errors)
        file.close()

def repl():

    print(f"Welcome to {pkg_name} v{version} on {platform.platform()}")
    print('Type ".help" for more information.')

    environment = Environment()

    while True:
        try:
            input_ = input(">>> ")

            if(input_.startswith(".")):

                match input_:
                    case ".help":
                        print("\n".join([
                            ".exit\texit the REPL",
                            ".help\tprint this help message",
                            ".load\tload TalonLang from a file into the REPL session",
                            ".save\tsave all evaluated commands in this REPL session to a file"
                        ]))

                    case ".exit":
                        break

                    case _:
                        print("invalid REPL keyword")

            else:
                lexer = Lexer(input_)
                parser = Parser(lexer)
                program = parser.parse_program()

                if len(parser.errors) > 0:
                    for error in parser.errors:
                        print(f"ERROR: {error}")
                else:
                    evaluated = eval(program, environment)
                    if evaluated is not None:
                        print(evaluated.inspect())

        except KeyboardInterrupt:
            print("\nkeyboardInterrupt")
    
repl()
# read_file("source.talon")
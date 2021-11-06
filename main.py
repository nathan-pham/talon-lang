from language.Lexer import Lexer
from language.Parser import Parser
from language.eval.Evaluator import eval

from utils.JSON import JSON

import platform
import sys

pkg_name = "Talon"
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

    print(f"{pkg_name} {version} on {platform.platform()}")
    print('Type "help", "copyright", "credits" or "license" for more information.')

    while True:
        try:
            input_ = input(">>> ")

            match input_:
                case ".exit":
                    break

                case _:
                    lexer = Lexer(input_)
                    parser = Parser(lexer)
                    program = parser.parse_program()

                    if len(parser.errors) > 0:
                        for error in parser.errors:
                            print(f"{error}")
                    else:
                        evaluated = eval(program)
                        if evaluated is not None:
                            print(evaluated.inspect())
                    

        except KeyboardInterrupt:
            print("\nkeyboard interrupt")
    
repl()
# read_file("source.talon")
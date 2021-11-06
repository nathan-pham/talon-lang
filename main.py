from os import environ
from language.Lexer import Lexer
from language.Parser import Parser

from language.eval.Environment import Environment
from language.eval.evaluator import eval

from utils.JSON import JSON

import platform
import sys

pkg_name = "TalonLang"
version = "0.0.1"

def talon_lang(input_, environment, inspect=True):
    lexer = Lexer(input_)
    parser = Parser(lexer)
    program = parser.parse_program()

    if len(parser.errors) > 0:
        for error in parser.errors:
            print(f"PARSER ERROR: {error}")
    else:
        evaluated = eval(program, environment)
        if evaluated and inspect: print(evaluated.inspect())

def repl():
    print(f"Welcome to {pkg_name} v{version} on {platform.platform()}")
    print('Type ".help" for more information.')

    environment = Environment()

    while True:
        try:
            input_ = input(">>> ")

            if(input_.startswith(".")):

                match input_.split(" ")[0]:
                    case ".help":
                        print("\n".join([
                            ".exit\texit the REPL",
                            ".help\tprint this help message",
                            ".load\tload TalonLang from a file into the REPL session",
                            ".save\tsave all evaluated commands in this REPL session to a file"
                        ]))

                    case ".exit":
                        break

                    case ".load":
                        file_name = input_.split(" ")[1]
                        with open(file_name, "r") as file:
                            file_contents = file.read().strip()
                            talon_lang(file_contents, environment)

                    case _:
                        print("invalid REPL keyword")

            else: talon_lang(input_, environment)

        except KeyboardInterrupt:
            print("\nkeyboardInterrupt")
    

if len(sys.argv) > 1:
    environment = Environment()
    with open(sys.argv[1], "r") as file:
        file_contents = file.read().strip()
        talon_lang(file_contents, environment, False)
else: repl()
from language.Lexer import Lexer
from language.Parser import Parser

from utils.JSON import JSON

import platform

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

    should_exit = False

    while not should_exit:
        input_string = input(">>> ")

        match input_string:
            case ".exit":
                should_exit = True

            case _:
                lexer = Lexer(input_string)

                while True:
                    token = lexer.next_token()
                    print(token)
                    if token.type_ == "EOF":
                        break

# repl()
read_file("source.talon")
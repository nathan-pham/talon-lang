from language.Lexer import Lexer

import platform

pkg_name = "Talon"
version = "0.0.1"

def read_file(path):
    with open(path, "r") as file:
        file_contents = file.read().strip()
        
        lexer = Lexer(file_contents)

        while lexer.char != 0:
            token = lexer.next_token()
            print(token)

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

                while lexer.char != 0:
                    token = lexer.next_token()
                    print(token)

repl()
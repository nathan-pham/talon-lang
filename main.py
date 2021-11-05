from monkey.Lexer import Lexer

def read_file(path):
    with open(path, "r") as file:
        file_contents = file.read().strip()
        
        lexer = Lexer(file_contents)

        while lexer.char != 0:
            token = lexer.next_token()
            print(token)

        file.close()

def repl():
    import platform

    version = "1.0.0"

    print(f"Monkey {version} on {platform.platform()}")
    print('Type "help", "copyright", "credits" or "license" for more information.')

    should_exit = False

    while not should_exit:
        input_string = input(">>> ")

        if input_string == "exit()":
            should_exit = True

        else:
            lexer = Lexer(input_string)

            while lexer.char != 0:
                token = lexer.next_token()
                print(token)

repl()
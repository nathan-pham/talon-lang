from monkey.Lexer import Lexer

with open("source.monkey") as file:
    file_contents = file.read().strip()
    
    tokens = []

    lexer = Lexer(file_contents)
    while lexer.char != 0:
        token = lexer.next_token()
        tokens.append(token)
        print(token)

    file.close()
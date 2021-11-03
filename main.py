from monkey.Lexer import Lexer

with open("source.monkey") as file:
    lexer = Lexer(file.read())
    file.close()
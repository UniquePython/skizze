from lexer import Lexer

source = """
let x = 10
let y = 20 + x
print(y)
"""

lexer = Lexer(source)
tokens = lexer.tokenize()
for tok in tokens:
    print(tok)

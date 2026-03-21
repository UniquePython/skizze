from skizze_lexer import SkizzeLexer

source = """
let x = 10
let y = 20 + x
print(y)
"""

lexer = SkizzeLexer(source)
tokens = lexer.tokenize()
for tok in tokens:
    print(tok)

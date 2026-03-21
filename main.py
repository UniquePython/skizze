from skizze_errors import SkizzeError
from skizze_lexer import SkizzeLexer

source = """
let x = 10
let y = 20 + x!
print(y)
"""

lexer = SkizzeLexer(source)
try:
    tokens = lexer.tokenize()
    for tok in tokens:
        print(tok)
except SkizzeError as e:
    print(e)
    exit(1)

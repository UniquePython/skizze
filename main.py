from skizze_ast import pprint_ast
from skizze_lexer import SkizzeLexer
from skizze_parser import SkizzeParser

src = """
let x = 10
let y = 20
fn add(a, b) {
    a + b
}
let result = add(x, y)
if result > 25 {
    print("big")
} else {
    print("small")
}
"""

tokens = SkizzeLexer(src).tokenize()
ast = SkizzeParser(tokens).parse()
for node in ast.statements:
    pprint_ast(node)

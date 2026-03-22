from skizze_errors import SkizzeError
from skizze_interpreter import SkizzeInterpreter
from skizze_lexer import SkizzeLexer
from skizze_parser import SkizzeParser

source = """
let x = 10
let y = 20

fn add(a, b)
{
    a + b
}

let result = add(x, y)

if result > 25 {
    print("big")
} else {
    print("small")
}

let i = 0

while i < 5 {
    print(i)
    i = i + 1
}
"""

try:
    lexer = SkizzeLexer(source)
    tokens = lexer.tokenize()

    parser = SkizzeParser(tokens)
    ast = parser.parse()

    interpreter = SkizzeInterpreter()
    interpreter.run(ast)
except SkizzeError as e:
    print(e)
    exit(1)

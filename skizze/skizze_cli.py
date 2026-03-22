import sys

from skizze.skizze_errors import SkizzeError
from skizze.skizze_interpreter import SkizzeInterpreter
from skizze.skizze_lexer import SkizzeLexer
from skizze.skizze_parser import SkizzeParser


def run_file(path):
    try:
        with open(path, "r") as f:
            source = f.read()
    except FileNotFoundError:
        print(f"skizze: file not found: '{path}'")
        sys.exit(1)

    try:
        tokens = SkizzeLexer(source).tokenize()
        ast = SkizzeParser(tokens).parse()
        SkizzeInterpreter().run(ast)
    except SkizzeError as e:
        print(e)
        sys.exit(1)


def main():
    if len(sys.argv) != 2:
        print("Usage: skizze <file.skz>")
        sys.exit(1)
    run_file(sys.argv[1])

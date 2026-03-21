from skizze_errors import SkizzeLexError
from skizze_token import SKIZZE_KEYWORDS as SK
from skizze_token import SkizzeToken as ST
from skizze_token import SkizzeTokenKind as STK


class SkizzeLexer:
    def __init__(self, source: str):
        self.source = source
        self.pos = 0  # current character index
        self.line = 1
        self.tokens = []

    def current(self):
        return None if self.pos >= len(self.source) else self.source[self.pos]

    def advance(self):
        self.pos += 1

    def peek(self):
        return None if self.pos + 1 >= len(self.source) else self.source[self.pos + 1]

    def skip_whitespace(self):
        while (
            self.current() is not None
            and self.current().isspace()
            and self.current() != "\n"
        ):
            self.advance()

    def read_number(self):
        seen_dot = False
        num = ""
        while self.current() is not None and (
            self.current().isdecimal() or (self.current() == "." and not seen_dot)
        ):
            if self.current() == ".":
                seen_dot = True
            num += self.current()
            self.advance()
        return ST(STK.NUMBER, float(num) if seen_dot else int(num), self.line)

    def read_string(self):
        self.advance()  # skip opening "
        string = ""
        while self.current() is not None and self.current() != '"':
            string += self.current()
            self.advance()
        self.advance()  # skip closing "
        return ST(STK.STRING, string, self.line)

    def read_ident(self):
        ident = ""
        while self.current() is not None and (
            self.current().isalnum() or self.current() == "_"
        ):
            ident += self.current()
            self.advance()
        kind = SK.get(ident, STK.IDENT)
        value = ident if kind == STK.IDENT else None
        return ST(kind, value, self.line)

    def tokenize(self):
        while self.current() is not None:
            self.skip_whitespace()
            curr = self.current()
            if curr is None:
                break
            if curr == "+":
                self.tokens.append(ST(STK.PLUS, "+", self.line))
                self.advance()
            elif curr == "-":
                self.tokens.append(ST(STK.MINUS, "-", self.line))
                self.advance()
            elif curr == "*":
                self.tokens.append(ST(STK.STAR, "*", self.line))
                self.advance()
            elif curr == "/":
                self.tokens.append(ST(STK.SLASH, "/", self.line))
                self.advance()
            elif curr == "=":
                if self.peek() == "=":
                    self.advance()
                    self.tokens.append(ST(STK.EQ, "==", self.line))
                    self.advance()
                else:
                    self.tokens.append(ST(STK.ASSIGN, "=", self.line))
                    self.advance()
            elif curr == "!":
                if self.peek() == "=":
                    self.advance()
                    self.tokens.append(ST(STK.NEQ, "!=", self.line))
                    self.advance()
                else:
                    raise SkizzeLexError("Unexpected character: '!'", self.line)
            elif curr == "<":
                if self.peek() == "=":
                    self.advance()
                    self.tokens.append(ST(STK.LTE, "<=", self.line))
                    self.advance()
                else:
                    self.tokens.append(ST(STK.LT, "<", self.line))
                    self.advance()
            elif curr == ">":
                if self.peek() == "=":
                    self.advance()
                    self.tokens.append(ST(STK.GTE, ">=", self.line))
                    self.advance()
                else:
                    self.tokens.append(ST(STK.GT, ">", self.line))
                    self.advance()
            elif curr == "(":
                self.tokens.append(ST(STK.LPAREN, "(", self.line))
                self.advance()
            elif curr == ")":
                self.tokens.append(ST(STK.RPAREN, ")", self.line))
                self.advance()
            elif curr == "{":
                self.tokens.append(ST(STK.LBRACE, "{", self.line))
                self.advance()
            elif curr == "}":
                self.tokens.append(ST(STK.RBRACE, "}", self.line))
                self.advance()
            elif curr == ",":
                self.tokens.append(ST(STK.COMMA, ",", self.line))
                self.advance()
            elif curr.isdecimal():
                self.tokens.append(self.read_number())
            elif curr == '"':
                self.tokens.append(self.read_string())
            elif curr.isalnum() or curr == "_":
                self.tokens.append(self.read_ident())
            elif curr == "\n":
                self.tokens.append(ST(STK.NEWLINE, "\n", self.line))
                self.line += 1
                self.advance()
        self.tokens.append(ST(STK.EOF))
        return self.tokens

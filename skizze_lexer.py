from skizze_token import SKIZZE_KEYWORDS as SK
from skizze_token import SkizzeToken as ST
from skizze_token import SkizzeTokenKind as STK


class SkizzeLexer:
    def __init__(self, source: str):
        self.source = source
        self.pos = 0  # current character index
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
        return ST(STK.NUMBER, float(num) if seen_dot else int(num))

    def read_string(self):
        self.advance()  # skip opening "
        string = ""
        while self.current() is not None and self.current() != '"':
            string += self.current()
            self.advance()
        self.advance()  # skip closing "
        return ST(STK.STRING, string)

    def read_ident(self):
        ident = ""
        while self.current() is not None and (
            self.current().isalnum() or self.current() == "_"
        ):
            ident += self.current()
            self.advance()
        kind = SK.get(ident, STK.IDENT)
        value = ident if kind == STK.IDENT else None
        return ST(kind, value)

    def tokenize(self):
        while self.current() is not None:
            self.skip_whitespace()
            curr = self.current()
            if curr is None:
                break
            if curr == "+":
                self.tokens.append(ST(STK.PLUS, "+"))
                self.advance()
            elif curr == "-":
                self.tokens.append(ST(STK.MINUS, "-"))
                self.advance()
            elif curr == "*":
                self.tokens.append(ST(STK.STAR, "*"))
                self.advance()
            elif curr == "/":
                self.tokens.append(ST(STK.SLASH, "/"))
                self.advance()
            elif curr == "=":
                if self.peek() == "=":
                    self.advance()
                    self.tokens.append(ST(STK.EQ, "=="))
                    self.advance()
                self.tokens.append(ST(STK.ASSIGN, "="))
                self.advance()
            elif curr == "!":
                if self.peek() == "=":
                    self.advance()
                    self.tokens.append(ST(STK.NEQ, "!="))
                    self.advance()
                else:
                    raise SyntaxError("Unexpected character: '!'")
            elif curr == "<":
                if self.peek() == "=":
                    self.advance()
                    self.tokens.append(ST(STK.LTE, "<="))
                    self.advance()
                self.tokens.append(ST(STK.LT, "<"))
                self.advance()
            elif curr == ">":
                if self.peek() == "=":
                    self.advance()
                    self.tokens.append(ST(STK.GTE, ">="))
                    self.advance()
                self.tokens.append(ST(STK.GT, ">"))
                self.advance()
            elif curr == "(":
                self.tokens.append(ST(STK.LPAREN, "("))
                self.advance()
            elif curr == ")":
                self.tokens.append(ST(STK.RPAREN, ")"))
                self.advance()
            elif curr == "{":
                self.tokens.append(ST(STK.LBRACE, "{"))
                self.advance()
            elif curr == "}":
                self.tokens.append(ST(STK.RBRACE, "}"))
                self.advance()
            elif curr == ",":
                self.tokens.append(ST(STK.COMMA, ","))
                self.advance()
            elif curr.isdecimal():
                self.tokens.append(self.read_number())
            elif curr == '"':
                self.tokens.append(self.read_string())
            elif curr.isalnum() or curr == "_":
                self.tokens.append(self.read_ident())
            elif curr == "\n":
                self.tokens.append(ST(STK.NEWLINE, "\n"))
                self.advance()
        self.tokens.append(ST(STK.EOF))
        return self.tokens

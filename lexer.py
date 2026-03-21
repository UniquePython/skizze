import skizze_token as st


class Lexer:
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
        return st.Token(st.TokenKind.NUMBER, float(num) if seen_dot else int(num))

    def read_string(self):
        self.advance()  # skip opening "
        string = ""
        while self.current() is not None and self.current() != '"':
            string += self.current()
            self.advance()
        self.advance()  # skip closing "
        return st.Token(st.TokenKind.STRING, string)

    def read_ident(self):
        ident = ""
        while self.current() is not None and (
            self.current().isalnum() or self.current() == "_"
        ):
            ident += self.current()
            self.advance()
        kind = st.KEYWORDS.get(ident, st.TokenKind.IDENT)
        value = ident if kind == st.TokenKind.IDENT else None
        return st.Token(kind, value)

    def tokenize(self):
        while self.current() is not None:
            self.skip_whitespace()
            curr = self.current()
            if curr is None:
                break
            if curr == "+":
                self.tokens.append(st.Token(st.TokenKind.PLUS, "+"))
                self.advance()
            elif curr == "-":
                self.tokens.append(st.Token(st.TokenKind.MINUS, "-"))
                self.advance()
            elif curr == "*":
                self.tokens.append(st.Token(st.TokenKind.STAR, "*"))
                self.advance()
            elif curr == "/":
                self.tokens.append(st.Token(st.TokenKind.SLASH, "/"))
                self.advance()
            elif curr == "=":
                if self.peek() == "=":
                    self.advance()
                    self.tokens.append(st.Token(st.TokenKind.EQ, "=="))
                    self.advance()
                self.tokens.append(st.Token(st.TokenKind.ASSIGN, "="))
                self.advance()
            elif curr == "!":
                if self.peek() == "=":
                    self.advance()
                    self.tokens.append(st.Token(st.TokenKind.NEQ, "!="))
                    self.advance()
                else:
                    raise SyntaxError("Unexpected character: '!'")
            elif curr == "<":
                if self.peek() == "=":
                    self.advance()
                    self.tokens.append(st.Token(st.TokenKind.LTE, "<="))
                    self.advance()
                self.tokens.append(st.Token(st.TokenKind.LT, "<"))
                self.advance()
            elif curr == ">":
                if self.peek() == "=":
                    self.advance()
                    self.tokens.append(st.Token(st.TokenKind.GTE, ">="))
                    self.advance()
                self.tokens.append(st.Token(st.TokenKind.GT, ">"))
                self.advance()
            elif curr == "(":
                self.tokens.append(st.Token(st.TokenKind.LPAREN, "("))
                self.advance()
            elif curr == ")":
                self.tokens.append(st.Token(st.TokenKind.RPAREN, ")"))
                self.advance()
            elif curr == "{":
                self.tokens.append(st.Token(st.TokenKind.LBRACE, "{"))
                self.advance()
            elif curr == "}":
                self.tokens.append(st.Token(st.TokenKind.RBRACE, "}"))
                self.advance()
            elif curr == ",":
                self.tokens.append(st.Token(st.TokenKind.COMMA, ","))
                self.advance()
            elif curr.isdecimal():
                self.tokens.append(self.read_number())
            elif curr == '"':
                self.tokens.append(self.read_string())
            elif curr.isalnum() or curr == "_":
                self.tokens.append(self.read_ident())
            elif curr == "\n":
                self.tokens.append(st.Token(st.TokenKind.NEWLINE, "\n"))
                self.advance()
        self.tokens.append(st.Token(st.TokenKind.EOF))
        return self.tokens

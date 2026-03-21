import skizze_ast as sast
from skizze_errors import SkizzeSyntaxError
from skizze_token import SkizzeToken as ST
from skizze_token import SkizzeTokenKind as STK


class SkizzeParser:
    def __init__(self, tokens: list[ST]):
        self.tokens = tokens
        self.pos = 0

    def current(self):
        if self.pos >= len(self.tokens):
            return self.tokens[-1]  # always EOF
        return self.tokens[self.pos]

    def advance(self):
        tok = self.current()
        self.pos += 1
        return tok

    def expect(self, kind):
        if self.current().type == kind:
            return self.advance()
        raise SkizzeSyntaxError(
            f"Expected {kind}, got {self.current().type}",
            self.current().line,
            self.current().col,
        )

    def skip_newlines(self):
        while self.current().type == STK.NEWLINE:
            self.advance()

    def parse(self):
        statements = []
        self.skip_newlines()
        while self.current().type != STK.EOF:
            statements.append(self.parse_statement())
            self.skip_newlines()
        return sast.SkizzeBlockNode(statements)

    def parse_statement(self):
        t = self.current().type
        if t == STK.LET:
            return self.parse_let()
        if t == STK.FN:
            return self.parse_fn()
        if t == STK.IF:
            return self.parse_if()
        if t == STK.WHILE:
            return self.parse_while()
        if t == STK.PRINT:
            return self.parse_print()
        return self.parse_expression()

    def parse_let(self):
        self.advance()
        name = self.expect(STK.IDENT).value
        self.expect(STK.ASSIGN)
        value = self.parse_expression()
        return sast.SkizzeLetNode(name, value)

    def parse_fn(self):
        self.advance()
        name = self.expect(STK.IDENT).value
        self.expect(STK.LPAREN)
        params = []
        while self.current().type != STK.RPAREN:
            params.append(self.expect(STK.IDENT).value)
            if self.current().type == STK.COMMA:
                self.advance()
        self.expect(STK.RPAREN)
        body = self.parse_block()
        return sast.SkizzeFnNode(name, params, body)

    def parse_if(self):
        self.advance()
        condition = self.parse_expression()
        then_block = self.parse_block()
        self.skip_newlines()
        else_block = None
        if self.current().type == STK.ELSE:
            self.advance()
            else_block = self.parse_block()
        return sast.SkizzeIfNode(condition, then_block, else_block)

    def parse_while(self):
        self.advance()
        condition = self.parse_expression()
        body = self.parse_block()
        return sast.SkizzeWhileNode(condition, body)

    def parse_print(self):
        self.advance()
        self.expect(STK.LPAREN)
        value = self.parse_expression()
        self.expect(STK.RPAREN)
        return sast.SkizzePrintNode(value)

    def parse_block(self):
        self.expect(STK.LBRACE)
        statements = []
        self.skip_newlines()
        while self.current().type not in {STK.RBRACE, STK.EOF}:
            statements.append(self.parse_statement())
            self.skip_newlines()
        self.expect(STK.RBRACE)
        return sast.SkizzeBlockNode(statements)

    def parse_expression(self):
        return self.parse_comparison()

    def parse_comparison(self):
        left = self.parse_additive()
        while self.current().type in {
            STK.EQ,
            STK.NEQ,
            STK.LT,
            STK.GT,
            STK.LTE,
            STK.GTE,
        }:
            op = self.advance().value
            right = self.parse_additive()
            left = sast.SkizzeBinOpNode(left, op, right)
        return left

    def parse_additive(self):
        left = self.parse_multiplicative()
        while self.current().type in {STK.PLUS, STK.MINUS}:
            op = self.advance().value
            right = self.parse_multiplicative()
            left = sast.SkizzeBinOpNode(left, op, right)
        return left

    def parse_multiplicative(self):
        left = self.parse_unary()
        while self.current().type in {STK.STAR, STK.SLASH}:
            op = self.advance().value
            right = self.parse_unary()
            left = sast.SkizzeBinOpNode(left, op, right)
        return left

    def parse_unary(self):
        if self.current().type == STK.MINUS:
            self.advance()
            return sast.SkizzeUnaryOpNode("-", self.parse_primary())
        else:
            return self.parse_primary()

    def parse_primary(self):
        if self.current().type == STK.NUMBER:
            tok = self.advance()
            return sast.SkizzeNumberNode(tok.value)
        elif self.current().type == STK.STRING:
            tok = self.advance()
            return sast.SkizzeStringNode(tok.value)
        elif self.current().type == STK.TRUE:
            self.advance()
            return sast.SkizzeBoolNode(True)
        elif self.current().type == STK.FALSE:
            self.advance()
            return sast.SkizzeBoolNode(False)
        elif self.current().type == STK.IDENT:
            tok = self.advance()
            if self.current().type == STK.LPAREN:
                # it's a call - parse args
                self.advance()  # skip (
                args = []
                while self.current().type != STK.RPAREN:
                    args.append(self.parse_expression())
                    if self.current().type == STK.COMMA:
                        self.advance()
                self.expect(STK.RPAREN)
                return sast.SkizzeCallNode(tok.value, args)
            return sast.SkizzeIdentNode(tok.value)
        elif self.current().type == STK.LPAREN:
            self.advance()  # skip (
            expr = self.parse_expression()  # recursively parse whatever's inside
            self.expect(STK.RPAREN)
            return expr  # return the inner node directly, parens are just grouping
        else:
            raise SkizzeSyntaxError(
                "Malformed input", self.current().line, self.current().col
            )

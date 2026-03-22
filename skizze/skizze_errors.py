class SkizzeError(Exception):
    def __init__(self, message, line=None, col=None):
        self.message = message
        self.line = line
        self.col = col

    def __str__(self):
        err = f"[Skizze {self.kind}]"
        if self.line:
            err += f" Line {self.line}"
        if self.col:
            err += f", Col {self.col}"
        err += f": {self.message}"
        return err


class SkizzeLexError(SkizzeError):
    kind = "LexError"


class SkizzeSyntaxError(SkizzeError):
    kind = "SyntaxError"


class SkizzeRuntimeError(SkizzeError):
    kind = "RuntimeError"

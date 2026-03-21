class SkizzeError(Exception):
    def __init__(self, message, line=None):
        self.message = message
        self.line = line

    def __str__(self):
        if self.line:
            return f"[Skizze {self.kind}] Line {self.line}: {self.message}"
        return f"[Skizze {self.kind}]: {self.message}"


class SkizzeLexError(SkizzeError):
    kind = "LexError"


class SkizzeSyntaxError(SkizzeError):
    kind = "SyntaxError"


class SkizzeRuntimeError(SkizzeError):
    kind = "RuntimeError"

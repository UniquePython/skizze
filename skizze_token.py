from enum import Enum, auto


class SkizzeTokenKind(Enum):
    # Literals
    NUMBER = auto()
    STRING = auto()
    BOOL = auto()

    # Identifiers / keywords
    IDENT = auto()
    LET = auto()
    FN = auto()
    IF = auto()
    ELSE = auto()
    WHILE = auto()
    PRINT = auto()
    TRUE = auto()
    FALSE = auto()

    # Operators
    PLUS = auto()
    MINUS = auto()
    STAR = auto()
    SLASH = auto()
    ASSIGN = auto()
    EQ = auto()
    NEQ = auto()
    LT = auto()
    GT = auto()
    LTE = auto()
    GTE = auto()

    # Delimiters
    LPAREN = auto()
    RPAREN = auto()
    LBRACE = auto()
    RBRACE = auto()
    COMMA = auto()

    # Structure
    NEWLINE = auto()
    EOF = auto()


SKIZZE_KEYWORDS = {
    "let": SkizzeTokenKind.LET,
    "fn": SkizzeTokenKind.FN,
    "if": SkizzeTokenKind.IF,
    "else": SkizzeTokenKind.ELSE,
    "while": SkizzeTokenKind.WHILE,
    "print": SkizzeTokenKind.PRINT,
    "true": SkizzeTokenKind.TRUE,
    "false": SkizzeTokenKind.FALSE,
}


class SkizzeToken:
    def __init__(self, type: SkizzeTokenKind, value=None, line=None):
        self.type = type
        self.value = value
        self.line = line

    def __repr__(self):
        return (
            f"SkizzeToken({self.type}, {self.value!r})"
            if self.value is not None
            else f"SkizzeToken({self.type})"
        )

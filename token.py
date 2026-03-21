from enum import Enum, auto


class TokenKind(Enum):
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


KEYWORDS = {
    "let": TokenKind.LET,
    "fn": TokenKind.FN,
    "if": TokenKind.IF,
    "else": TokenKind.ELSE,
    "while": TokenKind.WHILE,
    "print": TokenKind.PRINT,
    "true": TokenKind.TRUE,
    "false": TokenKind.FALSE,
}


class Token:
    def __init__(self, type: TokenKind, value=None):
        self.type = type
        self.value = value

    def __repr__(self):
        return (
            f"Token({self.type}, {self.value!r})"
            if self.value is not None
            else f"Token({self.type})"
        )

from dataclasses import dataclass, field
from typing import Optional


@dataclass
class SkizzeNumberNode:
    value: int | float


@dataclass
class SkizzeStringNode:
    value: str


@dataclass
class SkizzeBoolNode:
    value: bool


@dataclass
class SkizzeIdentNode:
    name: str


@dataclass
class SkizzeLetNode:
    name: str
    value: object  # any expr node


@dataclass
class SkizzeBinOpNode:
    left: object
    op: str
    right: object


@dataclass
class SkizzeUnaryOpNode:
    op: str
    operand: object


@dataclass
class SkizzeBlockNode:
    statements: list = field(default_factory=list)


@dataclass
class SkizzeIfNode:
    condition: object
    then_block: SkizzeBlockNode
    else_block: Optional[SkizzeBlockNode]


@dataclass
class SkizzeWhileNode:
    condition: object
    body: SkizzeBlockNode


@dataclass
class SkizzeFnNode:
    name: str
    params: list  # list of strings
    body: SkizzeBlockNode


@dataclass
class SkizzeCallNode:
    name: str
    args: list  # list of expr nodes


@dataclass
class SkizzePrintNode:
    value: object


def pprint_ast(node, indent=0):
    pad = "  " * indent
    name = type(node).__name__

    match node:
        case SkizzeBlockNode(statements=stmts):
            print(f"{pad}Block:")
            for s in stmts:
                pprint_ast(s, indent + 1)

        case SkizzeLetNode(name=n, value=v):
            print(f"{pad}Let {n!r} =")
            pprint_ast(v, indent + 1)

        case SkizzeFnNode(name=n, params=p, body=b):
            print(f"{pad}Fn {n!r} ({', '.join(p)})")
            pprint_ast(b, indent + 1)

        case SkizzeIfNode(condition=c, then_block=t, else_block=e):
            print(f"{pad}If:")
            pprint_ast(c, indent + 1)
            print(f"{pad}Then:")
            pprint_ast(t, indent + 1)
            if e:
                print(f"{pad}Else:")
                pprint_ast(e, indent + 1)

        case SkizzeWhileNode(condition=c, body=b):
            print(f"{pad}While:")
            pprint_ast(c, indent + 1)
            print(f"{pad}Body:")
            pprint_ast(b, indent + 1)

        case SkizzeBinOpNode(left=l, op=op, right=r):
            print(f"{pad}BinOp {op!r}")
            pprint_ast(l, indent + 1)
            pprint_ast(r, indent + 1)

        case SkizzeUnaryOpNode(op=op, operand=o):
            print(f"{pad}Unary {op!r}")
            pprint_ast(o, indent + 1)

        case SkizzeCallNode(name=n, args=args):
            print(f"{pad}Call {n!r}")
            for a in args:
                pprint_ast(a, indent + 1)

        case SkizzePrintNode(value=v):
            print(f"{pad}Print:")
            pprint_ast(v, indent + 1)

        case SkizzeIdentNode(name=n):
            print(f"{pad}Ident {n!r}")

        case SkizzeNumberNode(value=v):
            print(f"{pad}Number {v}")

        case SkizzeStringNode(value=v):
            print(f"{pad}String {v!r}")

        case SkizzeBoolNode(value=v):
            print(f"{pad}Bool {v}")

        case _:
            print(f"{pad}<unknown node: {name}>")

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

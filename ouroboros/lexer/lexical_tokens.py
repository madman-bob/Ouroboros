from abc import ABCMeta
from dataclasses import dataclass
from typing import List


class Token(metaclass=ABCMeta):
    pass


@dataclass(frozen=True)
class Identifier(Token):
    name: str

    def __str__(self):
        return self.name

    def __repr__(self):
        return "`{}`".format(self.name)

    def __bool__(self):
        return bool(self.name)


@dataclass(frozen=True)
class Constant(Token):
    value: object

    def __str__(self):
        return str(self.value)


@dataclass(frozen=True)
class IntToken(Constant):
    value: int


@dataclass(frozen=True)
class Statement(Token):
    terms: List[Token]


@dataclass(frozen=True)
class Block(Token):
    statements: List[Token]


@dataclass(frozen=True)
class ListStatement(Token):
    values: List[Statement]


@dataclass(frozen=True)
class Comment(Token):
    comment_text: str


@dataclass(frozen=True)
class StringStatement(Token):
    value: str


@dataclass(frozen=True)
class ImportStatement(Token):
    path: str


@dataclass(frozen=True)
class FunctionCall(Token):
    func: Token
    args: List[Token]

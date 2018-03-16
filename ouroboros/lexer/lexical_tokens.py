from abc import ABCMeta

from namedlist import namedtuple


class Token(metaclass=ABCMeta):
    pass


class Identifier(Token, namedtuple('Identifier', 'name')):
    def __str__(self):
        return self.name

    def __repr__(self):
        return "`{}`".format(self.name)

    def __bool__(self):
        return bool(self.name)


class Constant(Token, namedtuple('Constant', 'value')):
    def __str__(self):
        return str(self.value)


class IntToken(Constant):
    pass


class Statement(Token, namedtuple('Statement', ['terms'])):
    pass


class Block(Token, namedtuple('Block', ['statements'])):
    pass


class ListStatement(Token, namedtuple('ListStatement', ['values'])):
    pass


class Comment(Token, namedtuple('Comment', ['comment_text'])):
    pass


class StringStatement(Token, namedtuple('StringStatement', ['value'])):
    pass


class ImportStatement(Token, namedtuple('ImportStatement', ['path'])):
    pass

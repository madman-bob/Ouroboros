from abc import ABCMeta

from namedlist import namedtuple


class Sentence(metaclass=ABCMeta):
    pass


class Identifier(Sentence, namedtuple('Identifier', 'name')):
    def __str__(self):
        return self.name

    def __repr__(self):
        return "`{}`".format(self.name)

    def __bool__(self):
        return bool(self.name)


class ConstantSentence(Sentence, namedtuple('ConstantSentence', 'value')):
    def __str__(self):
        return str(self.value)


class IntToken(ConstantSentence):
    pass


class Statement(Sentence, namedtuple('Statement', ['terms'])):
    pass


class Block(Sentence, namedtuple('Block', ['statements'])):
    pass


class ListStatement(Sentence, namedtuple('ListStatement', ['values'])):
    pass


class Comment(Sentence, namedtuple('Comment', ['comment_text'])):
    pass


class StringStatement(Sentence, namedtuple('StringStatement', ['value'])):
    pass


class ImportStatement(Sentence, namedtuple('ImportStatement', ['path'])):
    pass

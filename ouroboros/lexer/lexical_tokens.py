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


Statement = namedtuple('Statement', ['terms'])

Block = namedtuple('Block', ['statements'])

ListStatement = namedtuple('ListStatement', ['values'])

Comment = namedtuple('Comment', ['comment_text'])

StringStatement = namedtuple('StringStatement', ['value'])

ImportStatement = namedtuple('ImportStatement', ['path'])

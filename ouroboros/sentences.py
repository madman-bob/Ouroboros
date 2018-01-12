from abc import ABCMeta

from namedlist import namedtuple

from ouroboros.scope import Scope


class Sentence(metaclass=ABCMeta):
    def eval(self, scope: Scope):
        pass


class Identifier(Sentence, namedtuple('Identifier', 'name')):
    def eval(self, scope: Scope):
        return scope[self]

    def __str__(self):
        return self.name

    def __repr__(self):
        return "`{}`".format(self.name)

    def __bool__(self):
        return bool(self.name)


class ConstantSentence(Sentence, namedtuple('ConstantSentence', 'value')):
    def eval(self, scope: Scope):
        return self.value

    def __str__(self):
        return str(self.value)


class IntToken(ConstantSentence):
    pass

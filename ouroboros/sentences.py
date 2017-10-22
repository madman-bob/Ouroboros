from abc import ABCMeta

from ouroboros.scope import Scope


class Sentence(metaclass=ABCMeta):
    def eval(self, scope: Scope):
        pass

    def __eq__(self, other):
        return type(self) == type(other) and self.__dict__ == other.__dict__


class Identifier(Sentence):
    def __init__(self, name):
        self.name = name

    def eval(self, scope: Scope):
        return scope[self]

    def __str__(self):
        return self.name

    def __repr__(self):
        return "`{}`".format(self.name)

    def __hash__(self):
        return hash(self.name)

    def __bool__(self):
        return bool(self.name)


class ConstantSentence(Sentence):
    def __init__(self, value):
        self.value = value

    def eval(self, scope: Scope):
        return self.value

    def __str__(self):
        return str(self.value)


class IntToken(ConstantSentence):
    pass

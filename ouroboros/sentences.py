from abc import ABCMeta
from functools import singledispatch

from namedlist import namedtuple

from ouroboros.scope import Scope


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


@singledispatch
def eval_sentence(sentence: object, scope: Scope) -> object:
    return sentence


@eval_sentence.register(Sentence)
def _(sentence: Sentence, scope: Scope) -> object:
    raise NotImplementedError("{!r} {!r}".format(sentence, scope))


@eval_sentence.register(Identifier)
def _(sentence: Identifier, scope: Scope) -> object:
    return scope[sentence]


@eval_sentence.register(ConstantSentence)
def _(sentence: ConstantSentence, scope: Scope) -> object:
    return sentence.value

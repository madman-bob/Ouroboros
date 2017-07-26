from ouroboros.evalable import Evalable
from ouroboros.scope import Scope


class Token(Evalable):
    def eval(self, scope: Scope):
        pass

    def __eq__(self, other):
        return type(self) == type(other) and self.__dict__ == other.__dict__


class Identifier(Token):
    def __init__(self, name):
        self.name = name

    def eval(self, scope: Scope):
        return scope[self]

    def __str__(self):
        return self.name

    def __hash__(self):
        return hash(self.name)


class IntToken(Token):
    def __init__(self, value):
        self.value = value

    def eval(self, scope: Scope):
        return self.value

    def __str__(self):
        return str(self.value)

from evalable import Evalable
from scope import Scope


class Token(Evalable):
    def eval(self, scope: Scope):
        pass

    def __eq__(self, other):
        return type(self) == type(other) and self.__dict__ == other.__dict__

from abc import ABCMeta, abstractmethod

from scope import Scope


class Evalable(metaclass=ABCMeta):
    @abstractmethod
    def eval(self, scope: Scope):
        pass

from ouroboros.sentences import Sentence
from ouroboros.scope import Scope


class Expression:
    def __init__(self, sentence: Sentence, scope: Scope):
        self.sentence = sentence
        self.scope = scope

    def eval(self) -> object:
        return self.sentence.eval(self.scope)

    def __repr__(self) -> str:
        return "{}({!r}, {!r})".format(self.__class__.__name__, self.sentence, self.scope)

from cached_property import cached_property
from more_itertools import peekable

from evalable import Evalable
from scope import Scope


class ContextBase(Evalable):
    whitespace = " \t\n"
    special_pretokens = ()

    def __init__(self, iterable, end_tokens=()):
        self.iterator = peekable(iterable)
        self.end_pretokens = end_tokens
        self.end_pretoken = None

        self.ast

    def splitter(self):
        """
        Yields pretokens generated from input iterator

        Splits pretokens based on whitespace characters, and on special_pretokens,
        yielding special_pretokens, but not whitespace

        Ends when the iterator is exhausted, or one of the end_pretokens are reached

        Currently only special_pretokens and end_pretokens of a single character are allowed
        """
        pretoken = ""
        for char in self.iterator:
            if char in self.whitespace:
                if pretoken:
                    yield pretoken
                    pretoken = ""
            elif char in self.end_pretokens:
                if pretoken:
                    yield pretoken
                self.end_pretoken = char
                return
            elif char in self.special_pretokens:
                if pretoken:
                    yield pretoken
                    pretoken = ""
                yield char
            else:
                pretoken += char
        if pretoken:
            yield pretoken

    def tokenizer(self, pretoken):
        """
        Given a string representation of a token, turn it into a token
        """
        return pretoken

    def token_stream(self):
        for pretoken in self.splitter():
            yield self.tokenizer(pretoken)

    @cached_property
    def ast(self):
        return list(self.token_stream())

    def eval(self, scope: Scope):
        pass

    def __repr__(self):
        return "{}([{}])".format(
            self.__class__.__name__,
            (
                "\n\t{}\n".format(",\n\t".join(str(token).replace("\n", "\n\t") for token in self.ast))
                if any(isinstance(token, ContextBase) for token in self.ast) else
                ", ".join(str(token) for token in self.ast)
            )
        )

    def __bool__(self):
        return bool(self.ast)

    def __iter__(self):
        yield from self.ast

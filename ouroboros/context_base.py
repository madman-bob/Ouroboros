from cached_property import cached_property
from more_itertools import peekable

from ouroboros.sentences import Sentence


class ContextSwitch:
    def __init__(self, start_pretoken, end_pretoken, context_class, allow_implicit_end=False):
        self.start_pretoken = start_pretoken
        self.end_pretoken = end_pretoken
        self.context_class = context_class
        self.allow_implicit_end = allow_implicit_end


class ContextBase(Sentence):
    whitespace = tuple(" \t\n")
    special_pretokens = ()
    context_switches = ()

    def __init__(self, iterable, end_tokens=()):
        self.iterator = peekable(iterable)
        self.end_pretokens = tuple(end_tokens)
        self.end_pretoken = None

        self.special_pretokens += tuple(context_switch.start_pretoken for context_switch in self.context_switches)
        self.special_pretokens += self.end_pretokens

        self.ast

    def splitter(self):
        """
        Yields pretokens generated from input iterator

        Splits pretokens based on whitespace characters, and on special_pretokens,
        yielding special_pretokens, but not whitespace

        Ends when the iterator is exhausted, or one of the end_pretokens are reached
        """
        if "" in self.special_pretokens:
            while self.iterator:
                yield ""
            return

        pretoken = ""
        for char in self.iterator:
            if char in self.whitespace:
                if pretoken:
                    yield pretoken
                    pretoken = ""
                continue

            pretoken += char

            special_pretoken = next((special_pretoken for special_pretoken in self.special_pretokens if pretoken.endswith(special_pretoken)), None)
            if special_pretoken is not None:
                if pretoken != special_pretoken:
                    yield pretoken[:len(pretoken) - len(special_pretoken)]
                pretoken = ""

            if special_pretoken in self.end_pretokens:
                self.end_pretoken = special_pretoken
                return

            if special_pretoken is not None:
                yield special_pretoken
        if pretoken:
            yield pretoken

    def tokenizer(self, pretoken):
        """
        Given a string representation of a token, turn it into a token
        """
        return pretoken

    def token_stream(self):
        for pretoken in self.splitter():
            context_switch = next((context_switch for context_switch in self.context_switches if context_switch.start_pretoken == pretoken), None)
            if context_switch is None:
                yield self.tokenizer(pretoken)
            else:
                new_context_end_pretokens = (context_switch.end_pretoken,)
                if context_switch.allow_implicit_end:
                    new_context_end_pretokens += self.end_pretokens

                new_context = context_switch.context_class(self.iterator, new_context_end_pretokens)
                yield new_context

                if context_switch.allow_implicit_end and new_context.end_pretoken in self.end_pretokens:
                    self.end_pretoken = new_context.end_pretoken
                    return

    @cached_property
    def ast(self):
        return list(self.token_stream())

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

from abc import ABCMeta

from more_itertools import peekable

from ouroboros.sentences import Sentence
from ouroboros.utils import cached_class_property


class ContextSwitch:
    def __init__(self, start_pretoken, end_pretoken, context_class, allow_implicit_end=False):
        self.start_pretoken = start_pretoken
        self.end_pretoken = end_pretoken
        self.context_class = context_class
        self.allow_implicit_end = allow_implicit_end


class Tokenizer:
    def __init__(self, iterable, whitespace, special_pretokens=(), end_tokens=()):
        self.iterator = peekable(iterable)
        self.end_pretokens = tuple(end_tokens)

        self.whitespace = whitespace
        self.special_pretokens = special_pretokens + self.end_pretokens

    def __iter__(self):
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

                yield special_pretoken

            if special_pretoken in self.end_pretokens:
                return

        if pretoken:
            yield pretoken


class ContextBase(Sentence, metaclass=ABCMeta):
    whitespace = tuple(" \t\n")
    special_pretokens = ()
    context_switches = ()

    @cached_class_property
    def context_switches_lookup(cls):
        return {context_switch.start_pretoken: context_switch for context_switch in cls.context_switches}

    @classmethod
    def tokenize(cls, iterable, end_tokens=()):
        tokenizer = Tokenizer(
            iterable=iterable,
            whitespace=cls.whitespace,
            special_pretokens=cls.special_pretokens + tuple(cls.context_switches_lookup),
            end_tokens=end_tokens
        )

        for token in tokenizer:
            if token not in cls.context_switches_lookup:
                yield token
            else:
                context_switch = cls.context_switches_lookup[token]
                new_context_end_pretokens = (context_switch.end_pretoken,)
                if context_switch.allow_implicit_end:
                    new_context_end_pretokens += end_tokens

                new_context = context_switch.context_class.parse(tokenizer.iterator, new_context_end_pretokens)
                yield new_context

                if context_switch.allow_implicit_end and new_context.end_pretoken in end_tokens:
                    yield new_context.end_pretoken
                    return

    @classmethod
    def parse_pretoken(cls, pretoken):
        return pretoken

    @classmethod
    def from_tokens(cls, tokens, end_pretoken=None):
        return cls(tokens, end_pretoken=end_pretoken)

    @classmethod
    def parse(cls, iterable, end_tokens=()):
        tokens = [
            cls.parse_pretoken(pretoken) if pretoken not in end_tokens else pretoken
            for pretoken in cls.tokenize(iterable, end_tokens)
        ]
        end_token = None

        if tokens and tokens[-1] in end_tokens:
            end_token = tokens.pop()

        return cls.from_tokens(tokens, end_pretoken=end_token)

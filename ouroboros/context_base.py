from abc import ABCMeta

from more_itertools import peekable

from namedlist import namedtuple

from ouroboros.sentences import Sentence
from ouroboros.utils import cached_class_property

ContextSwitch = namedtuple('ContextSwitch', [
    'start_token',
    'end_token',
    'context_class',
    ('allow_implicit_end', False),
    ('start_token_is_special', True),
])


class Tokenizer:
    def __init__(self, iterable, whitespace, special_tokens=(), end_tokens=()):
        self.iterator = peekable(iterable)
        self.end_tokens = tuple(end_tokens)

        self.whitespace = whitespace
        self.special_tokens = special_tokens + self.end_tokens

    def __iter__(self):
        """
        Yields tokens generated from input iterator

        Splits tokens based on whitespace characters, and on special_tokens,
        yielding special_tokens, but not whitespace

        Ends when the iterator is exhausted, or one of the end_tokens are reached
        """
        if "" in self.special_tokens:
            while self.iterator:
                yield ""
            return

        token = ""
        for char in self.iterator:
            if char in self.whitespace:
                if token:
                    yield token
                    token = ""
                continue

            token += char

            special_token = next((special_token for special_token in self.special_tokens if token.endswith(special_token)), None)
            if special_token is not None:
                if token != special_token:
                    yield token[:len(token) - len(special_token)]
                token = ""

                yield special_token

            if special_token in self.end_tokens:
                return

        if token:
            yield token


class ContextBase(Sentence, metaclass=ABCMeta):
    whitespace = tuple(" \t\n")
    special_tokens = ()
    context_switches = ()

    @cached_class_property
    def context_switches_lookup(cls):
        return {context_switch.start_token: context_switch for context_switch in cls.context_switches}

    @classmethod
    def tokenize(cls, iterable, end_tokens=()):
        tokenizer = Tokenizer(
            iterable=iterable,
            whitespace=cls.whitespace,
            special_tokens=cls.special_tokens + tuple(context_switch.start_token for context_switch in cls.context_switches if context_switch.start_token_is_special),
            end_tokens=end_tokens
        )

        for token in tokenizer:
            if token not in cls.context_switches_lookup:
                yield token
            else:
                context_switch = cls.context_switches_lookup[token]
                new_context_end_tokens = ()
                if context_switch.end_token is not None:
                    new_context_end_tokens += (context_switch.end_token,)
                if context_switch.allow_implicit_end:
                    new_context_end_tokens += end_tokens

                new_context, end_token = context_switch.context_class.parse(tokenizer.iterator, new_context_end_tokens)
                yield new_context

                if context_switch.allow_implicit_end and end_token in end_tokens:
                    yield end_token
                    return

    @classmethod
    def parse_token(cls, token):
        return token

    @classmethod
    def from_tokens(cls, tokens):
        return cls(tokens)

    @classmethod
    def parse(cls, iterable, end_tokens=()):
        tokens = [
            cls.parse_token(token) if token not in end_tokens else token
            for token in cls.tokenize(iterable, end_tokens)
        ]
        end_token = None

        if tokens and tokens[-1] in end_tokens:
            end_token = tokens.pop()

        return cls.from_tokens(tokens), end_token

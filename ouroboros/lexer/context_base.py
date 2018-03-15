from abc import ABCMeta

from namedlist import namedtuple

from ouroboros.sentences import Sentence
from ouroboros.lexer.chunker import Chunker
from ouroboros.utils import cached_class_property

ContextSwitch = namedtuple('ContextSwitch', [
    'start_token',
    'end_token',
    'context_class',
    ('allow_implicit_end', False),
    ('start_token_is_special', True),
])


class ContextBase(Sentence, metaclass=ABCMeta):
    whitespace = tuple(" \t\n")
    special_tokens = ()
    context_switches = ()

    @cached_class_property
    def context_switches_lookup(cls):
        return {context_switch.start_token: context_switch for context_switch in cls.context_switches}

    @classmethod
    def chunk(cls, iterable, end_tokens=()):
        chunker = Chunker(
            iterable=iterable,
            whitespace=cls.whitespace,
            special_tokens=cls.special_tokens + tuple(context_switch.start_token for context_switch in cls.context_switches if context_switch.start_token_is_special),
            end_tokens=end_tokens
        )

        for token in chunker:
            if token not in cls.context_switches_lookup:
                yield token
            else:
                context_switch = cls.context_switches_lookup[token]
                new_context_end_tokens = ()
                if context_switch.end_token is not None:
                    new_context_end_tokens += (context_switch.end_token,)
                if context_switch.allow_implicit_end:
                    new_context_end_tokens += end_tokens

                new_context, end_token = context_switch.context_class.parse(chunker.iterator, new_context_end_tokens)
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
            for token in cls.chunk(iterable, end_tokens)
        ]
        end_token = None

        if tokens and tokens[-1] in end_tokens:
            end_token = tokens.pop()

        return cls.from_tokens(tokens), end_token

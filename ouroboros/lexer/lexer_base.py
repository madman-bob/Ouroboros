from abc import ABCMeta
from dataclasses import dataclass
from typing import Optional, Type

from ouroboros.lexer.chunker import Chunker
from ouroboros.utils import cached_class_property


class LexerBase(metaclass=ABCMeta):
    whitespace = tuple(" \t\n")
    special_lexemes = ()
    context_switches = ()
    result_class = list

    @cached_class_property
    def context_switches_lookup(cls):
        return {context_switch.start_lexeme: context_switch for context_switch in cls.context_switches}

    @classmethod
    def chunk(cls, iterable, end_lexemes=()):
        chunker = Chunker(
            iterable=iterable,
            whitespace=cls.whitespace,
            special_lexemes=cls.special_lexemes + tuple(context_switch.start_lexeme for context_switch in cls.context_switches if context_switch.start_lexeme_is_special),
            end_lexemes=end_lexemes
        )

        for lexeme in chunker:
            if lexeme not in cls.context_switches_lookup:
                yield lexeme
            else:
                context_switch = cls.context_switches_lookup[lexeme]
                new_context_end_lexemes = ()
                if context_switch.end_lexeme is not None:
                    new_context_end_lexemes += (context_switch.end_lexeme,)
                if context_switch.allow_implicit_end:
                    new_context_end_lexemes += end_lexemes

                new_context, end_lexeme = context_switch.context_class.parse(chunker.iterator, new_context_end_lexemes)
                yield new_context

                if context_switch.allow_implicit_end and end_lexeme in end_lexemes:
                    yield end_lexeme
                    return

    @classmethod
    def parse_token(cls, lexeme):
        return lexeme

    @classmethod
    def from_tokens(cls, tokens):
        return cls.result_class(tokens)

    @classmethod
    def parse(cls, iterable, end_lexemes=()):
        tokens = [
            cls.parse_token(lexeme) if lexeme not in end_lexemes else lexeme
            for lexeme in cls.chunk(iterable, end_lexemes)
        ]
        end_lexeme = None

        if tokens and tokens[-1] in end_lexemes:
            end_lexeme = tokens.pop()

        return cls.from_tokens(tokens), end_lexeme


@dataclass
class ContextSwitch:
    start_lexeme: str
    end_lexeme: Optional[str]
    context_class: Type[LexerBase]
    allow_implicit_end: bool = False
    start_lexeme_is_special: bool = True

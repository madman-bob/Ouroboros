from ouroboros.lexer.lexical_tokens import Statement, Block, ListStatement, Comment, StringStatement, ImportStatement
from ouroboros.lexer.context_base import ContextBase, ContextSwitch
from ouroboros.sentences import Identifier, IntToken
from ouroboros.utils import cached_class_property


class StatementContext(ContextBase):
    special_lexemes = (".",)
    result_class = Statement

    @cached_class_property
    def context_switches(cls):
        return (
            ContextSwitch("{", "}", BlockContext),
            ContextSwitch("(", ")", StatementContext),
            ContextSwitch("[", "]", ListContext),
            ContextSwitch("#", "\n", CommentContext),
            ContextSwitch("/*", "*/", CommentContext),
            ContextSwitch('"', '"', StringContext),
            ContextSwitch("import", None, ImportContext, allow_implicit_end=True, start_lexeme_is_special=False),
        )

    @classmethod
    def parse_token(cls, lexeme):
        if not isinstance(lexeme, str):
            return lexeme
        elif lexeme.isdigit():
            return IntToken(int(lexeme))
        else:
            return Identifier(lexeme)

    def __bool__(self):
        return bool(self.terms)


class BlockContext(ContextBase):
    result_class = Block

    @cached_class_property
    def context_switches(cls):
        return (
            ContextSwitch("", ";", StatementContext, allow_implicit_end=True),
        )


class ListContext(ContextBase):
    result_class = ListStatement

    @cached_class_property
    def context_switches(cls):
        return (
            ContextSwitch("", ",", StatementContext, allow_implicit_end=True),
        )


class CommentContext(ContextBase):
    whitespace = ()
    result_class = Comment

    @classmethod
    def from_tokens(cls, tokens):
        assert len(tokens) <= 1
        return cls.result_class(tokens[0] if tokens else "")


class StringContext(ContextBase):
    whitespace = ()
    result_class = StringStatement

    @classmethod
    def from_tokens(cls, tokens):
        return cls.result_class("".join(tokens))


class ImportContext(ContextBase):
    whitespace = ()
    result_class = ImportStatement

    @classmethod
    def from_tokens(cls, tokens):
        return cls.result_class("".join(tokens))

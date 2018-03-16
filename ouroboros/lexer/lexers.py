from ouroboros.lexer.lexical_tokens import Identifier, IntToken, Statement, Block, ListStatement, Comment, StringStatement, ImportStatement
from ouroboros.lexer.lexer_base import LexerBase, ContextSwitch
from ouroboros.utils import cached_class_property


class StatementLexer(LexerBase):
    special_lexemes = (".",)
    result_class = Statement

    @cached_class_property
    def context_switches(cls):
        return (
            ContextSwitch("{", "}", BlockLexer),
            ContextSwitch("(", ")", StatementLexer),
            ContextSwitch("[", "]", ListLexer),
            ContextSwitch("#", "\n", CommentLexer),
            ContextSwitch("/*", "*/", CommentLexer),
            ContextSwitch('"', '"', StringLexer),
            ContextSwitch("import", None, ImportLexer, allow_implicit_end=True, start_lexeme_is_special=False),
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


class BlockLexer(LexerBase):
    result_class = Block

    @cached_class_property
    def context_switches(cls):
        return (
            ContextSwitch("", ";", StatementLexer, allow_implicit_end=True),
        )


class ListLexer(LexerBase):
    result_class = ListStatement

    @cached_class_property
    def context_switches(cls):
        return (
            ContextSwitch("", ",", StatementLexer, allow_implicit_end=True),
        )


class CommentLexer(LexerBase):
    whitespace = ()
    result_class = Comment

    @classmethod
    def from_tokens(cls, tokens):
        assert len(tokens) <= 1
        return cls.result_class(tokens[0] if tokens else "")


class StringLexer(LexerBase):
    whitespace = ()
    result_class = StringStatement

    @classmethod
    def from_tokens(cls, tokens):
        return cls.result_class("".join(tokens))


class ImportLexer(LexerBase):
    whitespace = ()
    result_class = ImportStatement

    @classmethod
    def from_tokens(cls, tokens):
        return cls.result_class("".join(tokens))

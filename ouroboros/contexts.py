from functools import singledispatch

from namedlist import namedtuple

from ouroboros.context_base import ContextBase, ContextSwitch
from ouroboros.sentences import Sentence, Identifier, IntToken, eval_sentence
from ouroboros.scope import Scope
from ouroboros.expressions import try_get_operator, unwrap_operator, Expression
from ouroboros.internal_types import ReturnType, ListType
from ouroboros.operators import Operator
from ouroboros.default_operators import ConstantExpression, Variable, FunctionExpression
from ouroboros.utils import cached_class_property


class StatementContext(ContextBase, namedtuple('StatementContext', ['terms'])):
    special_tokens = (".",)

    @cached_class_property
    def context_switches(cls):
        return (
            ContextSwitch("{", "}", BlockContext),
            ContextSwitch("(", ")", StatementContext),
            ContextSwitch("[", "]", ListContext),
            ContextSwitch("#", "\n", CommentContext),
            ContextSwitch("/*", "*/", CommentContext),
            ContextSwitch('"', '"', StringContext),
        )

    @classmethod
    def parse_token(cls, token):
        if isinstance(token, ContextBase):
            return token
        elif token.isdigit():
            return IntToken(int(token))
        else:
            return Identifier(token)

    def __bool__(self):
        return bool(self.terms)


class BlockContext(ContextBase, namedtuple('BlockContext', ['statements'])):
    @cached_class_property
    def context_switches(cls):
        return (
            ContextSwitch("", ";", StatementContext, allow_implicit_end=True),
        )


class ListContext(ContextBase, namedtuple('ListContext', ['values'])):
    @cached_class_property
    def context_switches(cls):
        return (
            ContextSwitch("", ",", StatementContext, allow_implicit_end=True),
        )


class CommentContext(ContextBase, namedtuple('CommentContext', ['comment_text'])):
    whitespace = ()

    @classmethod
    def from_tokens(cls, tokens):
        assert len(tokens) <= 1
        return cls(tokens[0] if tokens else "")


class StringContext(ContextBase, namedtuple('StringContext', ['value'])):
    whitespace = ()

    @classmethod
    def from_tokens(cls, tokens):
        return cls("".join(tokens))


@eval_sentence.register(StatementContext)
def _(sentence: StatementContext, scope: Scope) -> object:
    expressions = [try_get_operator(get_expression(token, scope)) for token in sentence.terms if not isinstance(token, CommentContext)]

    if not expressions:
        return ()

    return Operator.reduce(expressions)


@eval_sentence.register(BlockContext)
def _(sentence: BlockContext, scope: Scope) -> object:
    def call(arg: Expression):
        for subcontext in sentence.statements:
            result = eval_sentence(subcontext, scope)
            if isinstance(result, ReturnType):
                return result.return_value

    return FunctionExpression(call, scope, Identifier(''))


@eval_sentence.register(ListContext)
def _(sentence: ListContext, scope: Scope) -> object:
    return ListType([eval_sentence(statement, scope) for statement in sentence.values if statement])


@eval_sentence.register(CommentContext)
def _(sentence: CommentContext, scope: Scope) -> object:
    pass


@eval_sentence.register(StringContext)
def _(sentence: StringContext, scope: Scope) -> object:
    return sentence.value


@singledispatch
def get_expression(sentence: Sentence, scope: Scope) -> Expression:
    raise NotImplementedError("{!r} {!r}".format(sentence, scope))


@get_expression.register(Identifier)
def _(sentence: Identifier, scope: Scope) -> Expression:
    if sentence in scope:
        value = eval_sentence(sentence, scope)

        if isinstance(value, (Expression, Operator)):
            return Variable(sentence, scope, precedence=unwrap_operator(value).precedence)

    return Variable(sentence, scope)


@get_expression.register(IntToken)
@get_expression.register(ListContext)
@get_expression.register(StringContext)
@get_expression.register(StatementContext)
def _(sentence: Sentence, scope: Scope) -> Expression:
    return ConstantExpression(sentence, scope)


@get_expression.register(BlockContext)
def _(sentence: BlockContext, scope: Scope) -> Expression:
    return FunctionExpression(sentence, scope)

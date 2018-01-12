from functools import singledispatch

from namedlist import namedtuple

from ouroboros.context_base import ContextBase, ContextSwitch
from ouroboros.sentences import Sentence, Identifier, IntToken, eval_sentence
from ouroboros.scope import Scope
from ouroboros.expressions import Expression
from ouroboros.operators import Operator
from ouroboros.default_operators import ConstantExpression, Variable, FunctionExpression
from ouroboros.utils import cached_class_property


class StatementContext(ContextBase, namedtuple('StatementContext', ['terms', ('end_pretoken', None)])):
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
    def parse_pretoken(cls, pretoken):
        if isinstance(pretoken, ContextBase):
            return pretoken
        elif pretoken.isdigit():
            return IntToken(int(pretoken))
        else:
            return Identifier(pretoken)


class BlockContext(ContextBase, namedtuple('BlockContext', ['statements', ('end_pretoken', None)])):
    @cached_class_property
    def context_switches(cls):
        return (
            ContextSwitch("", ";", StatementContext, allow_implicit_end=True),
        )


class ListContext(ContextBase, namedtuple('ListContext', ['values', ('end_pretoken', None)])):
    @cached_class_property
    def context_switches(cls):
        return (
            ContextSwitch("", ",", StatementContext, allow_implicit_end=True),
        )


class CommentContext(ContextBase, namedtuple('CommentContext', ['comment_text', ('end_pretoken', None)])):
    whitespace = ()

    @classmethod
    def from_tokens(cls, tokens, end_pretoken=None):
        assert len(tokens) <= 1
        return cls(tokens[0] if tokens else "", end_pretoken=end_pretoken)


class StringContext(ContextBase, namedtuple('StringContext', ['value', ('end_pretoken', None)])):
    whitespace = ()

    @classmethod
    def from_tokens(cls, tokens, end_pretoken=None):
        return cls("".join(tokens), end_pretoken=end_pretoken)


@eval_sentence.register(StatementContext)
def _(sentence: StatementContext, scope: Scope) -> object:
    expressions = [get_expression(token, scope) for token in sentence.terms if not isinstance(token, CommentContext)]

    if not expressions:
        return ()

    return Operator.reduce(expressions)


@eval_sentence.register(BlockContext)
def _(sentence: BlockContext, scope: Scope) -> object:
    @FunctionExpression.from_python_function
    def call(arg: Expression):
        from ouroboros.default_scope import ReturnType
        inner_scope = Scope(parent_scope=scope)
        for subcontext in sentence.statements:
            result = eval_sentence(subcontext, inner_scope)
            if isinstance(result, ReturnType):
                return result.return_value

    return call


@eval_sentence.register(ListContext)
def _(sentence: ListContext, scope: Scope) -> object:
    return [eval_sentence(statement, scope) for statement in sentence.values]


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

        if isinstance(value, Expression):
            return Variable(sentence, scope, precedence=value.precedence)

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

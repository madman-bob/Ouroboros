from functools import singledispatch

from namedlist import namedtuple

from ouroboros.context_base import ContextBase, ContextSwitch
from ouroboros.sentences import Sentence, Identifier, IntToken
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

    def eval(self, scope: Scope):
        expressions = [get_expression(token, scope) for token in self.terms if not isinstance(token, CommentContext)]

        if not expressions:
            return ()

        return Operator.reduce(expressions)


class BlockContext(ContextBase, namedtuple('BlockContext', ['statements', ('end_pretoken', None)])):
    @cached_class_property
    def context_switches(cls):
        return (
            ContextSwitch("", ";", StatementContext, allow_implicit_end=True),
        )

    def eval(self, scope: Scope):
        @FunctionExpression.from_python_function
        def call(arg: Expression):
            from ouroboros.default_scope import ReturnType
            inner_scope = Scope(parent_scope=scope)
            for subcontext in self.statements:
                result = subcontext.eval(inner_scope)
                if isinstance(result, ReturnType):
                    return result.return_value

        return call


class ListContext(ContextBase, namedtuple('ListContext', ['values', ('end_pretoken', None)])):
    @cached_class_property
    def context_switches(cls):
        return (
            ContextSwitch("", ",", StatementContext, allow_implicit_end=True),
        )

    def eval(self, scope: Scope):
        return [statement.eval(scope) for statement in self.values]


class CommentContext(ContextBase, namedtuple('CommentContext', ['comment_text', ('end_pretoken', None)])):
    whitespace = ()

    @classmethod
    def from_tokens(cls, tokens, end_pretoken=None):
        assert len(tokens) <= 1
        return cls(tokens[0] if tokens else "", end_pretoken=end_pretoken)

    def eval(self, scope: Scope):
        pass


class StringContext(ContextBase, namedtuple('StringContext', ['value', ('end_pretoken', None)])):
    whitespace = ()

    @classmethod
    def from_tokens(cls, tokens, end_pretoken=None):
        return cls("".join(tokens), end_pretoken=end_pretoken)

    def eval(self, scope: Scope):
        return self.value


@singledispatch
def get_expression(sentence: Sentence, scope: Scope) -> Expression:
    raise NotImplementedError("{!r} {!r}".format(sentence, scope))


@get_expression.register(Identifier)
def _(sentence: Identifier, scope: Scope) -> Expression:
    if sentence in scope:
        value = sentence.eval(scope)

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

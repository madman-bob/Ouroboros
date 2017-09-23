from functools import reduce

from cached_property import cached_property

from ouroboros.context_base import ContextBase, ContextSwitch
from ouroboros.sentences import Identifier, IntToken
from ouroboros.scope import Scope
from ouroboros.expressions import Expression


class StatementContext(ContextBase):
    @cached_property
    def context_switches(self):
        return (
            ContextSwitch("{", "}", BlockContext),
            ContextSwitch("(", ")", StatementContext),
            ContextSwitch("[", "]", ListContext),
            ContextSwitch("#", "\n", CommentContext),
            ContextSwitch("/*", "*/", CommentContext),
            ContextSwitch('"', '"', StringContext),
        )

    def tokenizer(self, pretoken):
        if pretoken.isdigit():
            return IntToken(int(pretoken))
        else:
            return Identifier(pretoken)

    def eval(self, scope: Scope):
        ast = [token for token in self.ast if not isinstance(token, CommentContext)]

        if not ast:
            return ()

        ast = iter(ast)

        return reduce((lambda x, y: x(Expression(y, scope))), ast, next(ast).eval(scope))


class BlockContext(ContextBase):
    @cached_property
    def context_switches(self):
        return (
            ContextSwitch("", ";", StatementContext, allow_implicit_end=True),
        )

    def eval(self, scope: Scope):
        def call(arg: Expression):
            from ouroboros.default_scope import ReturnType
            inner_scope = Scope(parent_scope=scope)
            for subcontext in self.ast:
                result = subcontext.eval(inner_scope)
                if isinstance(result, ReturnType):
                    return result.return_value

        return call


class ListContext(ContextBase):
    @cached_property
    def context_switches(self):
        return (
            ContextSwitch("", ",", StatementContext, allow_implicit_end=True),
        )

    def eval(self, scope: Scope):
        return [statement.eval(scope) for statement in self]


class CommentContext(ContextBase):
    whitespace = ()

    def eval(self, scope: Scope):
        pass


class StringContext(ContextBase):
    whitespace = ()

    def eval(self, scope: Scope):
        return next(iter(self.ast), "")

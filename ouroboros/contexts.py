from functools import reduce

from cached_property import cached_property

from ouroboros.context_base import ContextBase, ContextSwitch
from ouroboros.evalable import Evalable
from ouroboros.scope import Scope
from ouroboros.tokens import Identifier, IntToken


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

        return reduce((lambda x, y: x(scope, y)), ast, next(ast).eval(scope))


class BlockContext(ContextBase):
    def token_stream(self):
        while self.iterator:
            statement = StatementContext(self.iterator, self.end_pretokens + (";",))

            if statement:
                yield statement

            if statement.end_pretoken != ";":
                return

    def eval(self, scope: Scope):
        def call(calling_scope: Scope, arg: Evalable):
            from ouroboros.default_scope import ReturnType
            inner_scope = Scope(parent_scope=scope)
            for subcontext in self.ast:
                result = subcontext.eval(inner_scope)
                if isinstance(result, ReturnType):
                    return result.return_value

        return call


class ListContext(ContextBase):
    special_pretokens = tuple(",")

    def token_stream(self):
        while self.iterator:
            statement = StatementContext(self.iterator, self.end_pretokens + (",",))

            if statement:
                yield statement

            if statement.end_pretoken != ",":
                return

    def eval(self, scope: Scope):
        return [statement.eval(scope) for statement in self]


class CommentContext(ContextBase):
    whitespace = ()
    special_pretokens = tuple("\n")

    def eval(self, scope: Scope):
        pass


class StringContext(ContextBase):
    whitespace = ()
    special_pretokens = tuple("\"")

    def eval(self, scope: Scope):
        return next(iter(self.ast), "")

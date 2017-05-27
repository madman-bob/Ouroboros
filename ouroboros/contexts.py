from functools import reduce

from context_base import ContextBase
from evalable import Evalable
from scope import Scope
from tokens import Identifier


class StatementContext(ContextBase):
    special_pretokens = ";{}()#\""

    def tokenizer(self, pretoken):
        if pretoken == "{":
            return BlockContext(self.iterator, ("}",))
        elif pretoken == "(":
            return StatementContext(self.iterator, ")")
        elif pretoken == "#":
            return CommentContext(self.iterator, "\n")
        elif pretoken == "\"":
            return StringContext(self.iterator, "\"")
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
            inner_scope = Scope(parent_scope=scope)
            for subcontext in self.ast:
                subcontext.eval(inner_scope)

        return call


class CommentContext(ContextBase):
    whitespace = ""
    special_pretokens = "\n"

    def eval(self, scope: Scope):
        pass


class StringContext(ContextBase):
    whitespace = ""
    special_pretokens = "\""

    def eval(self, scope: Scope):
        return next(iter(self.ast), "")
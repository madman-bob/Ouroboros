from functools import singledispatch

from namedlist import namedtuple

from ouroboros.scope import Scope
from ouroboros.lexer.lexical_tokens import Token, Identifier, Constant, Block, ListStatement, Comment, StringStatement
from ouroboros.expressions import Expression
from ouroboros.internal_types import ReturnType, ListType
from ouroboros.parser.parser import FunctionCall

SemanticToken = namedtuple('SemanticToken', ['token', 'scope'])


@singledispatch
def eval_sentence(token: object, scope: Scope) -> object:
    return token


@eval_sentence.register(Token)
def _(token: Token, scope: Scope) -> object:
    raise NotImplementedError("{!r} {!r}".format(token, scope))


@eval_sentence.register(Identifier)
def _(token: Identifier, scope: Scope) -> object:
    return scope[token]


@eval_sentence.register(Constant)
def _(token: Constant, scope: Scope) -> object:
    return token.value


@eval_sentence.register(Block)
def _(token: Block, scope: Scope) -> object:
    def call(arg: Expression, return_scope=False):
        inner_scope = Scope(parent_scope=scope)
        for subcontext in token.statements:
            result = eval_sentence(subcontext, inner_scope)
            if isinstance(result, ReturnType):
                if return_scope:
                    return result.return_value, inner_scope
                return result.return_value
        if return_scope:
            return None, inner_scope

    return call


@eval_sentence.register(ListStatement)
def _(token: ListStatement, scope: Scope) -> object:
    return ListType([eval_sentence(statement, scope) for statement in token.values if statement])


@eval_sentence.register(Comment)
def _(token: Comment, scope: Scope) -> object:
    pass


@eval_sentence.register(StringStatement)
def _(token: StringStatement, scope: Scope) -> object:
    return token.value


@eval_sentence.register(FunctionCall)
def _(token: FunctionCall, scope: Scope) -> object:
    func = eval_sentence(token.func, scope)

    result = func
    for arg in token.args:
        result = result(SemanticToken(arg, scope))

    return result


def eval_semantic_token(token):
    if isinstance(token, SemanticToken):
        return eval_sentence(token.token, token.scope)
    return token

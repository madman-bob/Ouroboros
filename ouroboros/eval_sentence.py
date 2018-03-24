from functools import singledispatch

from namedlist import namedtuple

from ouroboros.scope import Scope
from ouroboros.lexer.lexical_tokens import Token, Identifier, Constant, IntToken, Statement, Block, ListStatement, Comment, StringStatement, ImportStatement
from ouroboros.expressions import try_get_operator, unwrap_operator, Expression
from ouroboros.internal_types import ReturnType, ListType
from ouroboros.operators import Operator
from ouroboros.default_operators import ConstantExpression, Variable, FunctionExpression

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


@eval_sentence.register(Statement)
def _(token: Statement, scope: Scope) -> object:
    expressions = [try_get_operator(get_expression(token, scope)) for token in token.terms if not isinstance(token, Comment)]

    if not expressions:
        return ()

    return Operator.reduce(expressions)


@eval_sentence.register(Block)
def _(token: Block, scope: Scope) -> object:
    def call(arg: Expression):
        for subcontext in token.statements:
            result = eval_sentence(subcontext, scope)
            if isinstance(result, ReturnType):
                return result.return_value

    return FunctionExpression(call, scope, Identifier(''))


@eval_sentence.register(ListStatement)
def _(token: ListStatement, scope: Scope) -> object:
    return ListType([eval_sentence(statement, scope) for statement in token.values if statement])


@eval_sentence.register(Comment)
def _(token: Comment, scope: Scope) -> object:
    pass


@eval_sentence.register(StringStatement)
def _(token: StringStatement, scope: Scope) -> object:
    return token.value


@singledispatch
def get_expression(token: Token, scope: Scope) -> Expression:
    raise NotImplementedError("{!r} {!r}".format(token, scope))


@get_expression.register(Identifier)
def _(token: Identifier, scope: Scope) -> Expression:
    if token in scope:
        value = eval_sentence(token, scope)

        if isinstance(value, (Expression, Operator)):
            return Variable(token, scope, precedence=unwrap_operator(value).precedence)

    return Variable(token, scope)


@get_expression.register(IntToken)
@get_expression.register(ListStatement)
@get_expression.register(StringStatement)
@get_expression.register(Statement)
@get_expression.register(ImportStatement)
def _(token: Token, scope: Scope) -> Expression:
    return ConstantExpression(token, scope)


@get_expression.register(Block)
def _(token: Block, scope: Scope) -> Expression:
    return FunctionExpression(token, scope)


def eval_semantic_token(token: SemanticToken):
    return eval_sentence(token.token, token.scope)

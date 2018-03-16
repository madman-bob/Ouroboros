from functools import singledispatch

from ouroboros.scope import Scope
from ouroboros.sentences import Sentence, Identifier, ConstantSentence, IntToken
from ouroboros.lexer.lexical_tokens import Statement, Block, ListStatement, Comment, StringStatement, ImportStatement
from ouroboros.expressions import try_get_operator, unwrap_operator, Expression
from ouroboros.internal_types import ReturnType, ListType
from ouroboros.operators import Operator
from ouroboros.default_operators import ConstantExpression, Variable, FunctionExpression


@singledispatch
def eval_sentence(sentence: object, scope: Scope) -> object:
    return sentence


@eval_sentence.register(Sentence)
def _(sentence: Sentence, scope: Scope) -> object:
    raise NotImplementedError("{!r} {!r}".format(sentence, scope))


@eval_sentence.register(Identifier)
def _(sentence: Identifier, scope: Scope) -> object:
    return scope[sentence]


@eval_sentence.register(ConstantSentence)
def _(sentence: ConstantSentence, scope: Scope) -> object:
    return sentence.value


@eval_sentence.register(Statement)
def _(sentence: Statement, scope: Scope) -> object:
    expressions = [try_get_operator(get_expression(token, scope)) for token in sentence.terms if not isinstance(token, Comment)]

    if not expressions:
        return ()

    return Operator.reduce(expressions)


@eval_sentence.register(Block)
def _(sentence: Block, scope: Scope) -> object:
    def call(arg: Expression):
        for subcontext in sentence.statements:
            result = eval_sentence(subcontext, scope)
            if isinstance(result, ReturnType):
                return result.return_value

    return FunctionExpression(call, scope, Identifier(''))


@eval_sentence.register(ListStatement)
def _(sentence: ListStatement, scope: Scope) -> object:
    return ListType([eval_sentence(statement, scope) for statement in sentence.values if statement])


@eval_sentence.register(Comment)
def _(sentence: Comment, scope: Scope) -> object:
    pass


@eval_sentence.register(StringStatement)
def _(sentence: StringStatement, scope: Scope) -> object:
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
@get_expression.register(ListStatement)
@get_expression.register(StringStatement)
@get_expression.register(Statement)
@get_expression.register(ImportStatement)
def _(sentence: Sentence, scope: Scope) -> Expression:
    return ConstantExpression(sentence, scope)


@get_expression.register(Block)
def _(sentence: Block, scope: Scope) -> Expression:
    return FunctionExpression(sentence, scope)

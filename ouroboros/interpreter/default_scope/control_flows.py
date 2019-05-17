from functools import partial

from toolz import curry

from ouroboros.interpreter.internal_types import ReturnType, ElseBlock
from ouroboros.interpreter.eval_sentence import SemanticToken, eval_semantic_token
from ouroboros.interpreter.expressions import FunctionExpression, PrefixExpression, BinaryExpression
from ouroboros.interpreter.default_scope.base import in_default_scope

__all__ = ("if_statement", "else_block", "while_loop", "return_function")


@in_default_scope("if")
@FunctionExpression
@curry
def if_statement(condition: SemanticToken, body: SemanticToken):
    condition = eval_semantic_token(condition)
    body = eval_semantic_token(body)

    if isinstance(body, ElseBlock):
        if condition:
            result = body.true_block()
        else:
            result = body.false_block()

    elif condition:
        result = body()
    else:
        result = None

    if result is not None:
        return ReturnType(result)


@in_default_scope("else")
@partial(BinaryExpression, precedence=if_statement.precedence.create_after())
@curry
def else_block(true_block: SemanticToken, false_block: SemanticToken):
    return ElseBlock(eval_semantic_token(true_block), eval_semantic_token(false_block))


@in_default_scope("while")
@FunctionExpression
@curry
def while_loop(condition: SemanticToken, body: SemanticToken):
    while eval_semantic_token(condition):
        result = eval_semantic_token(body)()
        if result is not None:
            return ReturnType(result)


@in_default_scope("return")
@PrefixExpression
def return_function(return_value: SemanticToken):
    return ReturnType(eval_semantic_token(return_value))

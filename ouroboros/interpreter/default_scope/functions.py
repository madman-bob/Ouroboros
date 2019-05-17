from ouroboros.interpreter.internal_types import ObjectType
from ouroboros.interpreter.eval_sentence import SemanticToken, eval_semantic_token
from ouroboros.interpreter.expressions import FunctionExpression, PrefixExpression
from ouroboros.interpreter.default_scope.base import in_default_scope

__all__ = ("inner_print", "object_function")


@in_default_scope("print")
@FunctionExpression
def inner_print(token: SemanticToken):
    print(eval_semantic_token(token))


@in_default_scope("Object")
@PrefixExpression
def object_function(function):
    return ObjectType(eval_semantic_token(function)(return_scope=True)[1])

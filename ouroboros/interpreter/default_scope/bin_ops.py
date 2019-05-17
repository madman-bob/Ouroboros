from functools import partial, wraps
from operator import add, sub, mul, truediv, pow, mod, is_, eq, ne, lt, le, gt, ge, and_, or_, xor

from toolz import curry

from ouroboros.scope import Scope
from ouroboros.lexer.lexical_tokens import Identifier, Block
from ouroboros.interpreter.eval_sentence import SemanticToken, eval_semantic_token
from ouroboros.interpreter.expressions import FunctionExpression, BinaryExpression
from ouroboros.interpreter.default_scope.base import in_default_scope

__all__ = (
    "ouroboros_bin_op_from_python_bin_op",
    "assign",
    "ou_add", "ou_mul", "ou_pow", "ou_sub", "ou_div", "ou_mod",
    "ou_is", "ou_eq", "ou_ne", "ou_lt", "ou_le", "ou_gt", "ou_ge",
    "ou_contains",
    "ou_and", "ou_xor", "ou_or", "ou_not",
    "function",
    "get_attribute"
)


def ouroboros_bin_op_from_python_bin_op(func):
    @wraps(func)
    @curry
    def bin_op(left_token: SemanticToken, right_token: SemanticToken):
        return func(eval_semantic_token(left_token), eval_semantic_token(right_token))

    return bin_op


@in_default_scope("=")
@BinaryExpression
@curry
def assign(left_token: SemanticToken, right_token: SemanticToken):
    if not isinstance(left_token.token, Identifier):
        raise TypeError("Trying to assign to non-variable")

    assignment_value = eval_semantic_token(right_token)
    if left_token.token in left_token.scope:
        left_token.scope[left_token.token] = assignment_value
    else:
        left_token.scope.define(left_token.token, assignment_value)
    return assignment_value


ou_add = in_default_scope("+", assign.insert_after(ouroboros_bin_op_from_python_bin_op(add)))
ou_mul = in_default_scope("*", ou_add.insert_after(ouroboros_bin_op_from_python_bin_op(mul)))
ou_pow = in_default_scope("^", ou_mul.insert_after(ouroboros_bin_op_from_python_bin_op(pow)))

ou_sub = in_default_scope("-", ou_add.insert_after(ouroboros_bin_op_from_python_bin_op(sub)))
ou_div = in_default_scope("/", ou_mul.insert_after(ouroboros_bin_op_from_python_bin_op(truediv)))

ou_mod = in_default_scope("%", ou_add.insert_before(ouroboros_bin_op_from_python_bin_op(mod)))

ou_is = in_default_scope("is", assign.insert_after(ouroboros_bin_op_from_python_bin_op(is_)))
ou_eq = in_default_scope("==", ou_is.insert_equiv(ouroboros_bin_op_from_python_bin_op(eq)))
ou_ne = in_default_scope("!=", ou_eq.insert_equiv(ouroboros_bin_op_from_python_bin_op(ne)))
ou_lt = in_default_scope("<", ou_eq.insert_equiv(ouroboros_bin_op_from_python_bin_op(lt)))
ou_le = in_default_scope("<=", ou_eq.insert_equiv(ouroboros_bin_op_from_python_bin_op(le)))
ou_gt = in_default_scope(">", ou_eq.insert_equiv(ouroboros_bin_op_from_python_bin_op(gt)))
ou_ge = in_default_scope(">=", ou_eq.insert_equiv(ouroboros_bin_op_from_python_bin_op(ge)))

ou_contains = in_default_scope("in", ou_eq.insert_equiv(ouroboros_bin_op_from_python_bin_op(lambda a, b: a in b)))

ou_and = in_default_scope("and", ou_eq.insert_before(ouroboros_bin_op_from_python_bin_op(and_)))
ou_xor = in_default_scope("xor", ou_and.insert_before(ouroboros_bin_op_from_python_bin_op(xor)))
ou_or = in_default_scope("or", ou_and.insert_before(ouroboros_bin_op_from_python_bin_op(or_)))

ou_not = in_default_scope("not", FunctionExpression(lambda a: not eval_semantic_token(a)))


@in_default_scope("=>")
@assign.insert_after(right_associative=True)
@curry
def function(argument_name: SemanticToken, body: SemanticToken, arg: SemanticToken):
    if not isinstance(argument_name.token, Identifier):
        raise TypeError("Trying to assign to non-variable")

    scope = Scope(parent_scope=body.scope)
    argument_name = SemanticToken(argument_name.token, scope)
    body = SemanticToken(body.token, scope)

    assign(argument_name, arg)

    value = eval_semantic_token(body)

    if isinstance(body.token, Block):
        value = value()

    return value


@in_default_scope(".")
@partial(BinaryExpression, precedence=FunctionExpression.precedence)
@curry
def get_attribute(object: SemanticToken, attribute: SemanticToken):
    return eval_semantic_token(object).attributes[attribute.token]

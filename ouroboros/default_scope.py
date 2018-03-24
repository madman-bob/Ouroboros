from operator import add, sub, mul, truediv, pow, mod, is_, eq, ne, lt, le, gt, ge, and_, or_, xor
from functools import partial

from toolz import curry

from ouroboros.scope import Scope
from ouroboros.internal_types import ReturnType, ObjectType
from ouroboros.lexer.lexical_tokens import Identifier, Block
from ouroboros.eval_sentence import SemanticToken, eval_semantic_token
from ouroboros.default_operators import FunctionExpression, PrefixExpression, BinaryExpression

default_scope = Scope()


@curry
def in_default_scope(variable_name, value):
    default_scope.define(Identifier(variable_name), value)
    return value


in_default_scope("true", True)
in_default_scope("false", False)


@in_default_scope("print")
@FunctionExpression
def inner_print(expression: SemanticToken):
    print(eval_semantic_token(expression))


@in_default_scope("=")
@BinaryExpression
@curry
def assign(left_expression: SemanticToken, right_expression: SemanticToken):
    if not isinstance(left_expression.token, Identifier):
        raise TypeError("Trying to assign to non-variable")

    assignment_value = eval_semantic_token(right_expression)
    if left_expression.token in left_expression.scope:
        left_expression.scope[left_expression.token] = assignment_value
    else:
        left_expression.scope.define(left_expression.token, assignment_value)
    return assignment_value


ou_add = in_default_scope("+", assign.insert_after(BinaryExpression.ouroboros_bin_op_from_python_bin_op(add)))
ou_mul = in_default_scope("*", ou_add.insert_after(BinaryExpression.ouroboros_bin_op_from_python_bin_op(mul)))
ou_pow = in_default_scope("^", ou_mul.insert_after(BinaryExpression.ouroboros_bin_op_from_python_bin_op(pow)))

ou_sub = in_default_scope("-", ou_add.insert_after(BinaryExpression.ouroboros_bin_op_from_python_bin_op(sub)))
ou_div = in_default_scope("/", ou_mul.insert_after(BinaryExpression.ouroboros_bin_op_from_python_bin_op(truediv)))

ou_mod = in_default_scope("%", ou_add.insert_before(BinaryExpression.ouroboros_bin_op_from_python_bin_op(mod)))

ou_is = in_default_scope("is", assign.insert_after(BinaryExpression.ouroboros_bin_op_from_python_bin_op(is_)))
ou_eq = in_default_scope("==", ou_is.insert_equiv(BinaryExpression.ouroboros_bin_op_from_python_bin_op(eq)))
ou_ne = in_default_scope("!=", ou_eq.insert_equiv(BinaryExpression.ouroboros_bin_op_from_python_bin_op(ne)))
ou_lt = in_default_scope("<", ou_eq.insert_equiv(BinaryExpression.ouroboros_bin_op_from_python_bin_op(lt)))
ou_le = in_default_scope("<=", ou_eq.insert_equiv(BinaryExpression.ouroboros_bin_op_from_python_bin_op(le)))
ou_gt = in_default_scope(">", ou_eq.insert_equiv(BinaryExpression.ouroboros_bin_op_from_python_bin_op(gt)))
ou_ge = in_default_scope(">=", ou_eq.insert_equiv(BinaryExpression.ouroboros_bin_op_from_python_bin_op(ge)))

ou_contains = in_default_scope("in", ou_eq.insert_equiv(BinaryExpression.ouroboros_bin_op_from_python_bin_op(lambda a, b: a in b)))

ou_and = in_default_scope("and", ou_eq.insert_before(BinaryExpression.ouroboros_bin_op_from_python_bin_op(and_)))
ou_xor = in_default_scope("xor", ou_and.insert_before(BinaryExpression.ouroboros_bin_op_from_python_bin_op(xor)))
ou_or = in_default_scope("or", ou_and.insert_before(BinaryExpression.ouroboros_bin_op_from_python_bin_op(or_)))

ou_not = in_default_scope("not", FunctionExpression(lambda a: not eval_semantic_token(a)))


@in_default_scope("if")
@FunctionExpression
@curry
def if_statement(condition: SemanticToken, body: SemanticToken):
    if eval_semantic_token(condition):
        result = eval_semantic_token(body)(())
        if result is not None:
            return ReturnType(result)


@in_default_scope("while")
@FunctionExpression
@curry
def while_loop(condition: SemanticToken, body: SemanticToken):
    while eval_semantic_token(condition):
        result = eval_semantic_token(body)(())
        if result is not None:
            return ReturnType(result)


@in_default_scope("return")
@PrefixExpression
def return_function(return_value: SemanticToken):
    return ReturnType(eval_semantic_token(return_value))


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
        value = value(())

    return value


@in_default_scope("Object")
@PrefixExpression
def object_function(function):
    return ObjectType(eval_semantic_token(function)((), return_scope=True)[1])


@in_default_scope(".")
@partial(BinaryExpression, precedence=FunctionExpression.precedence)
@curry
def get_attribute(object: SemanticToken, attribute: SemanticToken):
    return eval_semantic_token(object).attributes[attribute.token]

from operator import add, sub, mul, truediv, pow, mod, is_, eq, ne, lt, le, gt, ge, and_, or_, xor

from toolz import curry

from ouroboros.scope import Scope
from ouroboros.sentences import Identifier
from ouroboros.expressions import Expression, eval_expression
from ouroboros.contexts import BlockContext
from ouroboros.default_operators import Variable, FunctionExpression, PrefixExpression, BinaryExpression

default_scope = Scope()


@curry
def in_default_scope(variable_name, value):
    default_scope.define(Identifier(variable_name), value)
    return value


in_default_scope("true", True)
in_default_scope("false", False)


@in_default_scope("print")
@FunctionExpression.from_python_function
def inner_print(expression: Expression):
    print(eval_expression(expression))


@in_default_scope("=")
@BinaryExpression
@curry
def assign(left_expression: Expression, right_expression: Expression):
    if not isinstance(left_expression, Variable):
        raise TypeError("Trying to assign to non-variable")

    assignment_value = eval_expression(right_expression)
    if left_expression.identifier in left_expression.scope:
        left_expression.scope[left_expression.identifier] = assignment_value
    else:
        left_expression.scope.define(left_expression.identifier, assignment_value)
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

ou_not = in_default_scope("not", FunctionExpression.from_python_function(lambda a: not eval_expression(a)))


@in_default_scope("if")
@FunctionExpression.from_python_function
@curry
def if_statement(condition: Expression, body: Expression):
    if eval_expression(condition):
        result = eval_expression(body)(())
        if result is not None:
            return ReturnType(result)


@in_default_scope("while")
@FunctionExpression.from_python_function
@curry
def while_loop(condition: Expression, body: Expression):
    while eval_expression(condition):
        result = eval_expression(body)(())
        if result is not None:
            return ReturnType(result)


class ReturnType:
    def __init__(self, return_value):
        self.return_value = return_value


@in_default_scope("return")
@PrefixExpression.from_python_function
def return_function(return_value: Expression):
    return ReturnType(eval_expression(return_value))


@in_default_scope("=>")
@assign.insert_after(right_associative=True)
def function(argument_name: Expression, body: Expression):
    if isinstance(body, FunctionExpression) and isinstance(body.block, BlockContext) and body.arg_name is None:
        return FunctionExpression(body.block, argument_name.scope, argument_name.identifier)
    return FunctionExpression(body, argument_name.scope, argument_name.identifier)

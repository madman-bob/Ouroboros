from operator import add, sub, mul, truediv, eq, ne, lt, le, gt, ge

from toolz import curry

from ouroboros.scope import Scope
from ouroboros.sentences import Identifier
from ouroboros.expressions import Expression
from ouroboros.contexts import BlockContext
from ouroboros.default_operators import Variable, FunctionExpression, BinaryExpression

default_scope = Scope()


@curry
def in_default_scope(variable_name, func):
    default_scope.define(Identifier(variable_name), func)
    return func


@in_default_scope("print")
@FunctionExpression.from_python_function
def inner_print(expression: Expression):
    print(expression.eval())


@in_default_scope("=")
@BinaryExpression
@curry
def assign(left_expression: Expression, right_expression: Expression):
    if not isinstance(left_expression, Variable):
        raise TypeError("Trying to assign to non-variable")

    assignment_value = right_expression.eval()
    if left_expression.identifier in left_expression.scope:
        left_expression.scope[left_expression.identifier] = assignment_value
    else:
        left_expression.scope.define(left_expression.identifier, assignment_value)
    return assignment_value


@curry
def bin_op(op, left_expression: Expression, right_expression: Expression):
    return op(left_expression.eval(), right_expression.eval())


bin_ops = {
    "+": add,
    "-": sub,
    "*": mul,
    "/": truediv,
    "==": eq,
    "!=": ne,
    "<": lt,
    "<=": le,
    ">": gt,
    ">=": ge,
}

for op_name, op in bin_ops.items():
    in_default_scope(op_name, BinaryExpression(bin_op(op)))


@in_default_scope("if")
@FunctionExpression.from_python_function
@curry
def if_statement(condition: Expression, body: Expression):
    if condition.eval():
        result = body.eval()(())
        if result is not None:
            return ReturnType(result)


@in_default_scope("while")
@FunctionExpression.from_python_function
@curry
def while_loop(condition: Expression, body: Expression):
    while condition.eval():
        result = body.eval()(())
        if result is not None:
            return ReturnType(result)


class ReturnType:
    def __init__(self, return_value):
        self.return_value = return_value


@in_default_scope("return")
@FunctionExpression.from_python_function
def return_function(return_value: Expression):
    return ReturnType(return_value.eval())


@in_default_scope("=>")
@BinaryExpression
def function(argument_name: Expression, body: Expression):
    if isinstance(body, FunctionExpression) and isinstance(body.block, BlockContext) and body.arg_name is None:
        return FunctionExpression(body.block, argument_name.scope, argument_name.identifier)
    return FunctionExpression(body, argument_name.scope, argument_name.identifier)

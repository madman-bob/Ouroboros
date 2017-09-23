from operator import add, sub, mul, truediv, eq, ne, lt, le, gt, ge

from toolz import curry

from ouroboros.scope import Scope
from ouroboros.sentences import Identifier
from ouroboros.expressions import Expression
from ouroboros.contexts import BlockContext

default_scope = Scope()


@curry
def in_default_scope(variable_name, func):
    default_scope.define(Identifier(variable_name), func)
    return func


@in_default_scope("print")
def inner_print(expression: Expression):
    print(expression.eval())


@in_default_scope("=")
@curry
def assign(left_expression: Expression, right_expression: Expression):
    assignment_value = right_expression.eval()
    if left_expression.sentence in left_expression.scope:
        left_expression.scope[left_expression.sentence] = assignment_value
    else:
        left_expression.scope.define(left_expression.sentence, assignment_value)
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
    in_default_scope(op_name, bin_op(op))


@in_default_scope("if")
@curry
def if_statement(condition: Expression, body: Expression):
    if condition.eval():
        result = body.eval()(())
        if result is not None:
            return ReturnType(result)


@in_default_scope("while")
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
def return_function(return_value: Expression):
    return ReturnType(return_value.eval())


@in_default_scope("=>")
@curry
def function(argument_name: Expression, body: Expression, argument: Expression):
    scope = Scope(parent_scope=body.scope)
    scope.define(argument_name.sentence, argument.eval())

    if isinstance(body.sentence, BlockContext):
        return body.sentence.eval(scope)(())
    else:
        return body.sentence.eval(scope)

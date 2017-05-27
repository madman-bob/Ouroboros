from operator import add, sub, mul, truediv, eq, ne, lt, le, gt, ge

from toolz import curry

from evalable import Evalable
from scope import Scope
from tokens import Identifier

default_scope = Scope()


@curry
def in_default_scope(variable_name, func):
    default_scope.define(Identifier(variable_name), func)
    return func


@in_default_scope("print")
def inner_print(scope: Scope, arg: Evalable):
    print(arg.eval(scope))


@curry
def bin_op(op, scope: Scope, arg: Evalable, inner_scope: Scope, inner_arg: Evalable):
    return op(arg.eval(scope), inner_arg.eval(inner_scope))


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

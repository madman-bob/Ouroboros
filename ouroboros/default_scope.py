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

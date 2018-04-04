from functools import singledispatch

from ouroboros.scope import Scope
from ouroboros.lexer.lexical_tokens import Identifier, Constant
from ouroboros.operators import Precedence, OperatorType


@singledispatch
def get_operator_type(token, operator_types: Scope, default_precedence: Precedence):
    return OperatorType(default_precedence, consumes_next=True)


@get_operator_type.register(Identifier)
def _(token: Identifier, operator_types: Scope, default_precedence: Precedence):
    return operator_types.get(token, OperatorType(default_precedence, consumes_next=True))


@get_operator_type.register(Constant)
def _(token: Constant, operator_types: Scope, default_precedence: Precedence):
    return OperatorType(default_precedence)

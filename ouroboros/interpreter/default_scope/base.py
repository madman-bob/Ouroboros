from toolz import curry

from ouroboros.scope import Scope
from ouroboros.lexer.lexical_tokens import Identifier

__all__ = ("default_scope", "in_default_scope")

default_scope = Scope()


@curry
def in_default_scope(variable_name, value):
    default_scope.define(Identifier(variable_name), value)
    return value

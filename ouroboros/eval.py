from ouroboros.contexts import StatementContext, BlockContext
from ouroboros.default_scope import default_scope

__all__ = ('ouroboros_eval', 'ouroboros_exec')


def ouroboros_eval(expression_string):
    return StatementContext.parse(expression_string).eval(default_scope)


def ouroboros_exec(expression_string):
    return BlockContext.parse(expression_string).eval(default_scope)(())

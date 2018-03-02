from ouroboros.scope import Scope
from ouroboros.sentences import eval_sentence
from ouroboros.contexts import StatementContext, BlockContext
from ouroboros.default_scope import default_scope

__all__ = ('ouroboros_eval', 'ouroboros_exec')


def ouroboros_eval(expression_string):
    statement, _ = StatementContext.parse(expression_string)
    return eval_sentence(statement, Scope(parent_scope=default_scope))


def ouroboros_exec(expression_string):
    block, _ = BlockContext.parse(expression_string)
    return eval_sentence(block, Scope(parent_scope=default_scope))(())

from ouroboros.sentences import eval_sentence
from ouroboros.contexts import StatementContext, BlockContext
from ouroboros.default_scope import default_scope

__all__ = ('ouroboros_eval', 'ouroboros_exec')


def ouroboros_eval(expression_string):
    return eval_sentence(StatementContext.parse(expression_string), default_scope)


def ouroboros_exec(expression_string):
    return eval_sentence(BlockContext.parse(expression_string), default_scope)(())

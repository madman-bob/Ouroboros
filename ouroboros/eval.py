from ouroboros.scope import Scope
from ouroboros.sentences import eval_sentence
from ouroboros.contexts import StatementContext, BlockContext
from ouroboros.default_scope import default_scope

__all__ = ('ouroboros_eval', 'ouroboros_exec')


def ouroboros_interpret(interpretation_context, expression_string):
    sentence, _ = interpretation_context.parse(expression_string)
    return eval_sentence(sentence, Scope(parent_scope=default_scope))


def ouroboros_eval(expression_string):
    return ouroboros_interpret(StatementContext, expression_string)


def ouroboros_exec(expression_string):
    return ouroboros_interpret(BlockContext, expression_string)(())

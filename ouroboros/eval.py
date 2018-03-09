from ouroboros.scope import Scope
from ouroboros.sentences import Identifier, eval_sentence
from ouroboros.contexts import StatementContext, BlockContext
from ouroboros.default_scope import default_scope

__all__ = ('ouroboros_eval', 'ouroboros_exec', 'ouroboros_import')


def ouroboros_interpret(interpretation_context, expression_string, **variables):
    sentence, _ = interpretation_context.parse(expression_string)
    return eval_sentence(sentence, Scope(
        local_scope={Identifier(identifier): value for identifier, value in variables.items()},
        parent_scope=default_scope
    ))


def ouroboros_eval(expression_string, **variables):
    return ouroboros_interpret(StatementContext, expression_string, **variables)


def ouroboros_exec(expression_string, **variables):
    return ouroboros_interpret(BlockContext, expression_string, **variables)(())


def ouroboros_import(file_handle, **variable):
    return ouroboros_exec(file_handle.read(), **variable)

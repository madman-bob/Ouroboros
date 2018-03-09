from os import path

from ouroboros.scope import Scope
from ouroboros.sentences import Identifier, eval_sentence
from ouroboros.contexts import StatementContext, BlockContext, ImportContext
from ouroboros.internal_types import ObjectType
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
    return_value, scope = ouroboros_interpret(BlockContext, expression_string, **variables)((), return_scope=True)

    if return_value is None:
        return ObjectType(scope)

    return return_value


def ouroboros_import(file_handle, **variable):
    file_path = path.realpath(file_handle.name)
    file_directory = path.dirname(file_path)

    return ouroboros_exec(
        file_handle.read(),
        __path__=file_path,
        __directory__=file_directory,
        **variable
    )


@eval_sentence.register(ImportContext)
def _(sentence: ImportContext, scope: Scope):
    with open(path.join(scope[Identifier("__directory__")], sentence.path + ".ou")) as import_file:
        return ouroboros_import(import_file)

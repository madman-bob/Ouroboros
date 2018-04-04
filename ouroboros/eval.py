from os import path

from ouroboros.scope import Scope
from ouroboros.eval_sentence import eval_sentence
from ouroboros.lexer.lexical_tokens import Identifier, ImportStatement
from ouroboros.lexer.lexers import StatementLexer, BlockLexer
from ouroboros.parser.parser import parse_token
from ouroboros.expressions import Expression, FunctionExpression
from ouroboros.internal_types import ObjectType
from ouroboros.default_scope import default_scope

__all__ = ('ouroboros_eval', 'ouroboros_exec', 'ouroboros_import')


def ouroboros_interpret(interpretation_context, expression_string, **variables):
    token, _ = interpretation_context.parse(expression_string)

    scope = Scope(
        local_scope={Identifier(identifier): value for identifier, value in variables.items()},
        parent_scope=default_scope
    )

    operator_types = Scope(parent_scope={
        key: value.get_operator_type()
        for key, value in scope.items()
        if isinstance(value, Expression)
    })

    token = parse_token(token, operator_types, FunctionExpression.precedence)

    return eval_sentence(token, scope)


def ouroboros_eval(expression_string, **variables):
    return ouroboros_interpret(StatementLexer, expression_string, **variables)


def ouroboros_exec(expression_string, **variables):
    return_value, scope = ouroboros_interpret(BlockLexer, expression_string, **variables)(return_scope=True)

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


@eval_sentence.register(ImportStatement)
def _(token: ImportStatement, scope: Scope):
    with open(path.join(scope[Identifier("__directory__")], token.path + ".ou")) as import_file:
        return ouroboros_import(import_file)

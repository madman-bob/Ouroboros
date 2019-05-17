from functools import singledispatch

from ouroboros.lexer.lexical_tokens import Identifier, Statement, Block, ListStatement, Comment, FunctionCall
from ouroboros.scope import Scope
from ouroboros.parser.operators import Precedence, OperatorType, Operator
from ouroboros.parser.precedences import get_operator_type


def _operator_func(token, operator_types, default_precedence):
    def f(*args):
        if args:
            if token == Identifier('=') and len(args) == 2:
                identifier = parse_token(args[0], operator_types, default_precedence)

                assert isinstance(identifier, Identifier)

                value = parse_token(args[1], operator_types, default_precedence)

                if identifier not in operator_types:
                    operator_types.define(identifier, get_operator_type(value, operator_types, default_precedence))

                args = [identifier, value]
            elif isinstance(token, FunctionCall):
                return Operator(
                    OperatorType(default_precedence, consumes_next=True),
                    _operator_func(FunctionCall(token.func, token.args + [
                        parse_token(arg, operator_types, default_precedence) for arg in args
                    ]), operator_types, default_precedence)
                )
            else:
                args = [parse_token(arg, operator_types, default_precedence) for arg in args]

            return Operator(
                OperatorType(default_precedence, consumes_next=True),
                _operator_func(
                    FunctionCall(parse_token(token, operator_types, default_precedence), args),
                    operator_types,
                    default_precedence
                )
            )

        else:
            return parse_token(token, operator_types, default_precedence)

    return f


@singledispatch
def parse_token(token, operator_types: Scope, default_precedence: Precedence):
    return token


@parse_token.register(Statement)
def _(statement: Statement, operator_types: Scope, default_precedence: Precedence):
    operators = [
        Operator(
            get_operator_type(token, operator_types, default_precedence),
            _operator_func(token, operator_types, default_precedence)
        )
        for token in statement.terms
        if not isinstance(token, Comment)
    ]

    if not operators:
        return ()

    return parse_token(Operator.reduce(operators), operator_types, default_precedence)


@parse_token.register(Block)
def _(token: Block, operator_types: Scope, default_precedence: Precedence):
    inner_operator_types = Scope(parent_scope=operator_types)
    return Block(list(filter(None, (
        parse_token(statement, inner_operator_types, default_precedence) for statement in token.statements
    ))))


@parse_token.register(ListStatement)
def _(token: ListStatement, operator_types: Scope, default_precedence: Precedence):
    return ListStatement([
        parse_token(value, operator_types, default_precedence) for value in token.values
    ])


@parse_token.register(Operator)
def _(token: Operator, operator_types: Scope, default_precedence: Precedence):
    return parse_token(token(), operator_types, default_precedence)

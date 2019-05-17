from unittest import TestCase

from ouroboros.lexer.lexical_tokens import Identifier, IntToken, Statement, Block
from ouroboros.scope import Scope
from ouroboros.parser.operators import Precedence, OperatorType
from ouroboros.parser.parser import FunctionCall, parse_token


class TestParsing(TestCase):
    scope = Scope({
        Identifier('return'): OperatorType(Precedence(-1), consumes_next=True),
        Identifier('='): OperatorType(Precedence(1), consumes_previous=True, consumes_next=True),
        Identifier('+'): OperatorType(Precedence(2), consumes_previous=True, consumes_next=True),
        Identifier('*'): OperatorType(Precedence(3), consumes_previous=True, consumes_next=True),
        Identifier('f'): OperatorType(Precedence(4), consumes_next=True)
    })

    def test_basic_parsing(self):
        self.assertEqual(
            parse_token(
                Statement([Identifier('f'), IntToken(1), IntToken(2)]),
                self.scope,
                Precedence(0)
            ),
            FunctionCall(Identifier('f'), [IntToken(1), IntToken(2)])
        )

    def test_basic_precedence_parsing(self):
        self.assertEqual(
            parse_token(
                Statement([IntToken(1), Identifier('+'), IntToken(2)]),
                self.scope,
                Precedence(0)
            ),
            FunctionCall(Identifier('+'), [IntToken(1), IntToken(2)])
        )

    def test_binary_operator_function_parsing_interaction(self):
        self.assertEqual(
            parse_token(
                Statement([Identifier('f'), IntToken(1), Identifier('+'), Identifier('f'), IntToken(2)]),
                self.scope,
                Precedence(0)
            ),
            FunctionCall(Identifier('+'), [
                FunctionCall(Identifier('f'), [IntToken(1)]),
                FunctionCall(Identifier('f'), [IntToken(2)])
            ])
        )

    def test_prefix_parsing(self):
        self.assertEqual(
            parse_token(
                Statement([Identifier('return'), Identifier('f'), IntToken(1)]),
                self.scope,
                Precedence(0)
            ),
            FunctionCall(Identifier('return'), [
                FunctionCall(Identifier('f'), [IntToken(1)])
            ])
        )

    def test_nested_statements(self):
        self.assertEqual(
            parse_token(
                Statement([Identifier('1'), Identifier('*'), Statement([Identifier('2'), Identifier('+'), Identifier('3')])]),
                self.scope,
                Precedence(0)
            ),
            FunctionCall(Identifier('*'), [Identifier('1'), FunctionCall(Identifier('+'), [Identifier('2'), Identifier('3')])])
        )

    def test_nested_precedence_parsing(self):
        self.assertEqual(
            parse_token(
                Statement([IntToken(1), Identifier('+'), IntToken(2), Identifier('*'), IntToken(3)]),
                self.scope,
                Precedence(0)
            ),
            FunctionCall(Identifier('+'), [IntToken(1), FunctionCall(Identifier('*'), [IntToken(2), IntToken(3)])])
        )

    def test_block_parsing(self):
        self.assertEqual(
            parse_token(
                Block([
                    Statement([Identifier('x'), Identifier('='), IntToken(1)]),
                    Statement([Identifier('x'), Identifier('='), Identifier('x'), Identifier('+'), IntToken(1)])
                ]),
                self.scope,
                Precedence(0)
            ),
            Block([
                FunctionCall(Identifier('='), [Identifier('x'), IntToken(1)]),
                FunctionCall(Identifier('='), [Identifier('x'), FunctionCall(Identifier('+'), [Identifier('x'), IntToken(1)])])
            ])
        )

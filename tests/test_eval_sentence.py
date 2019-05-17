from unittest import TestCase

from toolz import curry

from ouroboros.scope import Scope
from ouroboros.lexer.lexical_tokens import Identifier, IntToken, Block, FunctionCall
from ouroboros.eval_sentence import eval_sentence, eval_semantic_token


class TestEvalToken(TestCase):
    @staticmethod
    @curry
    def assign(semantic_token, value):
        identifier, scope = semantic_token.token, semantic_token.scope
        scope[identifier] = eval_semantic_token(value)

    def test_eval_constant(self):
        self.assertEqual(
            eval_sentence(IntToken(1), Scope({})),
            1
        )

    def test_eval_identifier(self):
        self.assertEqual(
            eval_sentence(Identifier('x'), Scope({Identifier('x'): 1})),
            1
        )

    def test_eval_function_call(self):
        self.assertEqual(
            eval_sentence(
                FunctionCall(
                    Identifier('f'),
                    [IntToken(1), IntToken(2)]
                ),
                Scope({
                    Identifier('f'): lambda x: lambda y: eval_semantic_token(x) + eval_semantic_token(y)
                })
            ),
            3
        )

    def test_eval_block(self):
        scope = Scope({
            Identifier('x'): 1,
            Identifier('+'): lambda x: lambda y: eval_semantic_token(x) + eval_semantic_token(y),
            Identifier('='): self.assign
        })

        func = eval_sentence(
            Block([
                FunctionCall(
                    Identifier('='),
                    [
                        Identifier('x'),
                        FunctionCall(
                            Identifier('+'),
                            [Identifier('x'), IntToken(1)]
                        )
                    ]
                )
            ]),
            scope
        )

        self.assertEqual(scope[Identifier('x')], 1)
        func()
        self.assertEqual(scope[Identifier('x')], 2)
        func()
        self.assertEqual(scope[Identifier('x')], 3)

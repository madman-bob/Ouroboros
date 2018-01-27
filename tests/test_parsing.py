from unittest import TestCase

from ouroboros.sentences import Identifier, IntToken
from ouroboros.contexts import StatementContext, BlockContext, ListContext, CommentContext, StringContext


class TestParsing(TestCase):
    def test_basic_parsing(self):
        statement, end_token = StatementContext.parse("Hello world")

        terms = [Identifier("Hello"), Identifier("world")]

        self.assertIsInstance(statement, StatementContext)
        self.assertEqual(statement.terms, terms)
        self.assertEqual(end_token, None)

        self.assertEqual(
            statement,
            StatementContext(terms)
        )

    def test_int_parsing(self):
        statement, _ = StatementContext.parse("x = 1")
        self.assertEqual(
            statement,
            StatementContext([Identifier("x"), Identifier("="), IntToken(1)])
        )

    def test_context_switching(self):
        statement, _ = StatementContext.parse("x = 1 /* Set the variable to 1 */")
        self.assertEqual(
            statement,
            StatementContext([
                Identifier("x"),
                Identifier("="),
                IntToken(1),
                CommentContext(" Set the variable to 1 ")
            ])
        )

    def test_block_parsing(self):
        block, _ = BlockContext.parse("x = 1; y = 2; z = 3")
        self.assertEqual(
            block,
            BlockContext([
                StatementContext([Identifier("x"), Identifier("="), IntToken(1)]),
                StatementContext([Identifier("y"), Identifier("="), IntToken(2)]),
                StatementContext([Identifier("z"), Identifier("="), IntToken(3)])
            ])
        )

    def test_list_parsing(self):
        statement, _ = StatementContext.parse("l = [1, 2, 3]")
        self.assertEqual(
            statement,
            StatementContext([
                Identifier("l"),
                Identifier("="),
                ListContext([
                    StatementContext([IntToken(1)]),
                    StatementContext([IntToken(2)]),
                    StatementContext([IntToken(3)])
                ])
            ])
        )

    def test_inline_comment_parsing(self):
        block, _ = BlockContext.parse("x = 1; # Set the variable to 1")
        self.assertEqual(
            block,
            BlockContext([
                StatementContext([Identifier("x"), Identifier("="), IntToken(1)]),
                StatementContext([CommentContext(' Set the variable to 1')])
            ])
        )

    def test_block_comment_parsing(self):
        block, _ = BlockContext.parse("""
            /*
                Set the variable to 1
            */
            x = 1;
        """)
        self.assertEqual(
            block,
            BlockContext(statements=[
                StatementContext(terms=[
                    CommentContext(comment_text='\n                Set the variable to 1\n            '),
                    Identifier("x"),
                    Identifier("="),
                    IntToken(value=1)
                ]),
                StatementContext(terms=[])
            ])
        )

    def test_string_parsing(self):
        for string in ["Hello, world", ""]:
            with self.subTest(string=string):
                statement, _ = StatementContext.parse('x = "{}"'.format(string))
                self.assertEqual(
                    statement,
                    StatementContext(terms=[
                        Identifier("x"),
                        Identifier("="),
                        StringContext(value=string)
                    ])
                )

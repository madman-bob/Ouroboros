from unittest import TestCase

from ouroboros.sentences import Identifier, IntToken
from ouroboros.contexts import StatementContext, BlockContext, ListContext, CommentContext, StringContext


class TestParsing(TestCase):
    def test_basic_parsing(self):
        statement = StatementContext.parse("Hello world")

        terms = [Identifier("Hello"), Identifier("world")]

        self.assertIsInstance(statement, StatementContext)
        self.assertEqual(statement.terms, terms)
        self.assertEqual(statement.end_pretoken, None)

        self.assertEqual(
            statement,
            StatementContext(terms)
        )

    def test_int_parsing(self):
        self.assertEqual(
            StatementContext.parse("x = 1"),
            StatementContext([Identifier("x"), Identifier("="), IntToken(1)])
        )

    def test_context_switching(self):
        self.assertEqual(
            StatementContext.parse("x = 1 /* Set the variable to 1 */"),
            StatementContext([
                Identifier("x"),
                Identifier("="),
                IntToken(1),
                CommentContext(" Set the variable to 1 ", end_pretoken="*/")
            ])
        )

    def test_block_parsing(self):
        self.assertEqual(
            BlockContext.parse("x = 1; y = 2; z = 3"),
            BlockContext([
                StatementContext([Identifier("x"), Identifier("="), IntToken(1)], end_pretoken=';'),
                StatementContext([Identifier("y"), Identifier("="), IntToken(2)], end_pretoken=';'),
                StatementContext([Identifier("z"), Identifier("="), IntToken(3)])
            ])
        )

    def test_list_parsing(self):
        self.assertEqual(
            StatementContext.parse("l = [1, 2, 3]"),
            StatementContext([
                Identifier("l"),
                Identifier("="),
                ListContext([
                    StatementContext([IntToken(1)], end_pretoken=','),
                    StatementContext([IntToken(2)], end_pretoken=','),
                    StatementContext([IntToken(3)], end_pretoken=']')
                ], end_pretoken=']')
            ])
        )

    def test_inline_comment_parsing(self):
        self.assertEqual(
            BlockContext.parse("x = 1; # Set the variable to 1"),
            BlockContext([
                StatementContext([Identifier("x"), Identifier("="), IntToken(1)], end_pretoken=';'),
                StatementContext([CommentContext(' Set the variable to 1')])
            ])
        )

    def test_block_comment_parsing(self):
        self.assertEqual(
            BlockContext.parse("""
                /*
                    Set the variable to 1
                */
                x = 1;
            """),
            BlockContext(statements=[
                StatementContext(terms=[
                    CommentContext(comment_text='\n                    Set the variable to 1\n                ', end_pretoken='*/'),
                    Identifier("x"),
                    Identifier("="),
                    IntToken(value=1)
                ], end_pretoken=';'),
                StatementContext(terms=[], end_pretoken=None)
            ], end_pretoken=None)
        )

    def test_string_parsing(self):
        for string in ["Hello, world", ""]:
            with self.subTest(string=string):
                self.assertEqual(
                    StatementContext.parse('x = "{}"'.format(string)),
                    StatementContext(terms=[
                        Identifier("x"),
                        Identifier("="),
                        StringContext(value=string, end_pretoken='"')
                    ], end_pretoken=None)
                )

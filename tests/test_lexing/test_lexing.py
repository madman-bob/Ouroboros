from unittest import TestCase

from ouroboros.lexer.lexical_tokens import Identifier, IntToken, Statement, Block, ListStatement, Comment, StringStatement, ImportStatement
from ouroboros.lexer.lexers import StatementLexer, BlockLexer


class TestLexing(TestCase):
    def test_basic_lexing(self):
        statement, end_token = StatementLexer.parse("Hello world")

        terms = [Identifier("Hello"), Identifier("world")]

        self.assertIsInstance(statement, Statement)
        self.assertEqual(statement.terms, terms)
        self.assertEqual(end_token, None)

        self.assertEqual(
            statement,
            Statement(terms)
        )

    def test_int_lexing(self):
        statement, _ = StatementLexer.parse("x = 1")
        self.assertEqual(
            statement,
            Statement([Identifier("x"), Identifier("="), IntToken(1)])
        )

    def test_context_switching(self):
        statement, _ = StatementLexer.parse("x = 1 /* Set the variable to 1 */")
        self.assertEqual(
            statement,
            Statement([
                Identifier("x"),
                Identifier("="),
                IntToken(1),
                Comment(" Set the variable to 1 ")
            ])
        )

    def test_block_lexing(self):
        block, _ = BlockLexer.parse("x = 1; y = 2; z = 3")
        self.assertEqual(
            block,
            Block([
                Statement([Identifier("x"), Identifier("="), IntToken(1)]),
                Statement([Identifier("y"), Identifier("="), IntToken(2)]),
                Statement([Identifier("z"), Identifier("="), IntToken(3)])
            ])
        )

    def test_list_lexing(self):
        statement, _ = StatementLexer.parse("l = [1, 2, 3]")
        self.assertEqual(
            statement,
            Statement([
                Identifier("l"),
                Identifier("="),
                ListStatement([
                    Statement([IntToken(1)]),
                    Statement([IntToken(2)]),
                    Statement([IntToken(3)])
                ])
            ])
        )

    def test_inline_comment_lexing(self):
        block, _ = BlockLexer.parse("x = 1; # Set the variable to 1")
        self.assertEqual(
            block,
            Block([
                Statement([Identifier("x"), Identifier("="), IntToken(1)]),
                Statement([Comment(' Set the variable to 1')])
            ])
        )

    def test_block_comment_lexing(self):
        block, _ = BlockLexer.parse("""
            /*
                Set the variable to 1
            */
            x = 1;
        """)
        self.assertEqual(
            block,
            Block(statements=[
                Statement(terms=[
                    Comment(comment_text='\n                Set the variable to 1\n            '),
                    Identifier("x"),
                    Identifier("="),
                    IntToken(value=1)
                ]),
                Statement(terms=[])
            ])
        )

    def test_string_lexing(self):
        for string in ["Hello, world", ""]:
            with self.subTest(string=string):
                statement, _ = StatementLexer.parse('x = "{}"'.format(string))
                self.assertEqual(
                    statement,
                    Statement(terms=[
                        Identifier("x"),
                        Identifier("="),
                        StringStatement(value=string)
                    ])
                )

    def test_import_lexing(self):
        block, _ = BlockLexer.parse("""
            x = import some_path;
        """)
        self.assertEqual(
            block,
            Block(statements=[
                Statement(terms=[
                    Identifier("x"),
                    Identifier("="),
                    ImportStatement(path="some_path")
                ]),
                Statement(terms=[])
            ])
        )

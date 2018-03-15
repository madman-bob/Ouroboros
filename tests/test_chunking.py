from unittest import TestCase

from ouroboros.lexer.context_base import Chunker


class TestChunker(TestCase):
    def test_basic_chunking(self):
        self.assertEqual(
            list(Chunker("Hello world", " ")),
            ["Hello", "world"]
        )

    def test_whitespace(self):
        self.assertEqual(
            list(Chunker(
                """
                    Hello world
                    Here are some more tokens

                    With  weird   spacing
                """,
                " \n"
            )),
            [
                "Hello", "world",
                "Here", "are", "some", "more", "tokens",
                "With", "weird", "spacing"
            ]
        )

    def test_special_tokens(self):
        self.assertEqual(
            list(Chunker(
                """
                    (multiple)tokens
                    only-one-token
                """,
                " \n",
                tuple("()")
            )),
            ["(", "multiple", ")", "tokens", "only-one-token"]
        )

    def test_multi_character_special_tokens(self):
        self.assertEqual(
            list(Chunker(
                """
                    /*Multiline comment*/
                """,
                " \n",
                ("/*", "*/")
            )),
            ["/*", "Multiline", "comment", "*/"]
        )

    def test_end_tokens(self):
        self.assertEqual(
            list(Chunker(
                """
                STOP!
                These tokens not reached
                """,
                " \n",
                end_tokens="!"
            )),
            ["STOP", "!"]
        )

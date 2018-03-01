from unittest import TestCase

from ouroboros.context_base import Tokenizer


class TestTokenizer(TestCase):
    def test_basic_tokenization(self):
        self.assertEqual(
            list(Tokenizer("Hello world", " ")),
            ["Hello", "world"]
        )

    def test_whitespace(self):
        self.assertEqual(
            list(Tokenizer(
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
            list(Tokenizer(
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
            list(Tokenizer(
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
            list(Tokenizer(
                """
                STOP!
                These tokens not reached
                """,
                " \n",
                end_tokens="!"
            )),
            ["STOP", "!"]
        )

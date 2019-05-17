from enum import Enum
from contextlib import redirect_stdout
from io import StringIO
from unittest import TestCase

from ouroboros import ouroboros_exec


class TestComments(TestCase):
    class CommentType(Enum):
        inline = "inline"
        multiline = "multiline"

    @staticmethod
    def get_exec_output(expression_string):
        example_output = StringIO()
        with redirect_stdout(example_output):
            ouroboros_exec(expression_string)
        return example_output.getvalue()

    def test_inline(self):
        self.assertEqual(
            self.get_exec_output("""
                # This is a comment
            """),
            ""
        )

    def test_multiline(self):
        self.assertEqual(
            self.get_exec_output("""
                /*
                    This is a comment
                */
            """),
            ""
        )

    def test_comments_ignored(self):
        with self.subTest(type=self.CommentType.inline):
            self.assertNotEqual(
                ouroboros_exec("""
                    # return 1;
                """),
                1
            )

        with self.subTest(type=self.CommentType.multiline):
            self.assertNotEqual(
                ouroboros_exec("""
                    /*
                        return 1;
                    */
                """),
                1
            )

    def test_comments_end(self):
        with self.subTest(type=self.CommentType.inline):
            self.assertEqual(
                ouroboros_exec("""
                    # return 1;
                    return 0;
                """),
                0
            )

        with self.subTest(type=self.CommentType.multiline):
            self.assertEqual(
                ouroboros_exec("""
                    /*
                        return 1;
                    */
                    return 0;
                """),
                0
            )

    def test_comments_inside_statement(self):
        with self.subTest(type=self.CommentType.inline):
            self.assertEqual(
                ouroboros_exec("""
                    return # 1
                        0;
                """),
                0
            )

        with self.subTest(type=self.CommentType.multiline):
            self.assertEqual(
                ouroboros_exec("""
                    return /*
                        1
                    */ 0;
                """),
                0
            )

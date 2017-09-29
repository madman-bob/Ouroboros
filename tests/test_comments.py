from enum import Enum
from unittest import TestCase

from ouroboros import ouroboros_exec


class TestComments(TestCase):
    class CommentType(Enum):
        inline = "inline"
        multiline = "multiline"

    def test_inline(self):
        self.assertIsNone(ouroboros_exec("""
            # This is a comment
        """))

    def test_multiline(self):
        self.assertIsNone(ouroboros_exec("""
            /*
                This is a comment
            */
        """))

    def test_comments_ignored(self):
        with self.subTest(type=self.CommentType.inline):
            self.assertIsNone(ouroboros_exec("""
                # return 1;
            """))

        with self.subTest(type=self.CommentType.multiline):
            self.assertIsNone(ouroboros_exec("""
                /*
                    return 1;
                */
            """))

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

from contextlib import redirect_stdout
from io import StringIO
from unittest import TestCase

from ouroboros import ouroboros_exec


class TestExamples(TestCase):
    @staticmethod
    def run_example(example_path):
        example_output = StringIO()
        with redirect_stdout(example_output), open("../examples/" + example_path) as example_file:
            ouroboros_exec(example_file.read())
        return example_output.getvalue()

    def test_basic_arithmetic(self):
        self.assertEqual(
            self.run_example("basic-arithmetic.ou"),
            (
                "1 + 1 =\n"
                "2\n"
                "2 - 1 =\n"
                "1\n"
                "2 * 3 =\n"
                "6\n"
                "12 / 4 =\n"
                "3.0\n"
            )
        )

    def test_hello_world(self):
        self.assertEqual(
            self.run_example("basic/hello_world.ou"),
            "Hello, world\n"
        )

    def test_comments(self):
        self.assertEqual(
            self.run_example("basic/comments.ou"),
            "Hello\n"
        )

    def test_if_statement(self):
        self.assertEqual(
            self.run_example("basic/if_statement.ou"),
            "Hello\n"
        )

    def test_while_loop(self):
        self.assertEqual(
            self.run_example("basic/while_loop.ou"),
            "".join(str(n) + "\n" for n in [1, 1, 2, 3, 5, 8])
        )

    def test_function(self):
        self.assertEqual(
            self.run_example("basic/function.ou"),
            "Hello\n"
        )

    def test_function_argument(self):
        self.assertEqual(
            self.run_example("basic/function_argument.ou"),
            "Hello, world\n"
        )

    def test_function_arguments(self):
        self.assertEqual(
            self.run_example("basic/function_arguments.ou"),
            "3\n"
        )

    def test_function_return_value(self):
        self.assertEqual(
            self.run_example("basic/function_return_value.ou"),
            "3\n"
        )

    def test_lists(self):
        self.assertEqual(
            self.run_example("list.ou"),
            "[0, 1, 2, 3, 4]\n"
        )

    def test_strings(self):
        self.assertEqual(
            self.run_example("strings.ou"),
            "String concatenation works\n"
        )

    def test_variables(self):
        self.assertEqual(
            self.run_example("variables.ou"),
            (
                "Variable assignment works\n"
                "Variable modification works\n"
            )
        )

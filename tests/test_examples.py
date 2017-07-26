from contextlib import redirect_stdout
from io import StringIO
from unittest import TestCase

from ouroboros.contexts import BlockContext
from ouroboros.scope import Scope
from ouroboros.default_scope import default_scope


class TestExamples(TestCase):
    @staticmethod
    def run_example(example_path):
        example_output = StringIO()
        with redirect_stdout(example_output), open("../examples/" + example_path) as example_file:
            BlockContext(example_file.read()).eval(default_scope)(Scope(), ())
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

    def test_functions(self):
        self.assertEqual(
            self.run_example("functions.ou"),
            (
                "After function definition, before function call\n"
                "Functions work\n"
                "Call functions multiple times\n"
                "Functions work\n"
                "Assignment in functions work\n"
                "Variables in outer scope can be modified\n"
                "This line is run\n"
                "Return value\n"
                "Passed in as an argument\n"
                "Multiple arguments\n"
                "Double return value\n"
            )
        )

    def test_hello_world(self):
        self.assertEqual(
            self.run_example("hello-world.ou"),
            "Hello, world\n"
        )

    def test_if_statement(self):
        self.assertEqual(
            self.run_example("if-statement.ou"),
            (
                "Entered first if\n"
                "Return value\n"
            )
        )

    def test_lists(self):
        self.assertEqual(
            self.run_example("list.ou"),
            "[0, 1, 2, 3, 4]\n"
        )

    def test_loops(self):
        self.assertEqual(
            self.run_example("loops.ou"),
            (
                "Basic loop:\n"
                "0\n"
                "1\n"
                "2\n"
                "3\n"
                "4\n"
                "5\n"
                "6\n"
                "7\n"
                "8\n"
                "9\n"
                "Fibonacci numbers:\n"
                "1\n"
                "1\n"
                "2\n"
                "3\n"
                "5\n"
                "8\n"
                "13\n"
                "21\n"
                "34\n"
                "55\n"
                "89\n"
                "144\n"
                "233\n"
            )
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
                "Weird stuff works\n"
            )
        )

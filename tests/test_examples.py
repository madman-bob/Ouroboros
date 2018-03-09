import os
from contextlib import redirect_stdout
from io import StringIO
from unittest import TestCase

from ouroboros import ouroboros_exec


class TestExamples(TestCase):
    examples_directory = "../examples/"

    @classmethod
    def find_examples(cls):
        for root, dirs, files in os.walk(cls.examples_directory):
            for file_name in files:
                yield os.path.join(root, file_name)

    @classmethod
    def run_example(cls, example_path):
        example_output = StringIO()
        with redirect_stdout(example_output), open(os.path.join(cls.examples_directory, example_path)) as example_file:
            ouroboros_exec(example_file.read())
        return example_output.getvalue()

    example_outputs = {
        "basic/hello_world.ou": "Hello, world\n",
        "basic/comments.ou": "Hello\n",
        "basic/if_statement.ou": "Hello\n",
        "basic/while_loop.ou": "".join(str(n) + "\n" for n in [1, 1, 2, 3, 5, 8]),
        "basic/function.ou": "Hello\n",
        "basic/function_argument.ou": "Hello, world\n",
        "basic/function_arguments.ou": "3\n",
        "basic/function_return_value.ou": "3\n",
        "basic/objects.ou": "".join(str(line) + "\n" for line in [[0, 0], [1, 10], [1, 10, 100], [2, 0, 25]]),
        "basic/import.ou": "Hello, world\n2\n3\n",
        "basic/import_object.ou": "",
        "basic/import_custom.ou": "",
        "intermediate/closure.ou": "".join(str(n) + "\n" for n in [1, 2, 3, 1, 2, 4, 3]),
        "intermediate/currying.ou": "3\n4\n5\n",
        "intermediate/first_class_functions.ou": "Hello\nHello\n",
        "intermediate/primes.ou": "".join(str(n) + "\n" for n in [2, 3, 4, 5, 7, 9, 11, 13, 17, 19, 23, 25, 29, 31, 37, 41, 43, 47, 49, 53, 59, 61, 67, 71, 73, 79, 83, 89, 97]),
        "intermediate/fibonacci.ou": "55\n55\n",
        "intermediate/brainfuck.ou": "2\n4\n",
        "advanced/double_return.ou": "55\n"
    }

    def test_find_examples(self):
        expected_examples = {os.path.abspath(os.path.join(self.examples_directory, example_path)) for example_path in self.example_outputs.keys()}
        found_examples = {os.path.abspath(example_path) for example_path in self.find_examples()}

        self.assertEqual(expected_examples, found_examples)

    def test_examples(self):
        for example_path, example_output in self.example_outputs.items():
            with self.subTest(example_path=example_path):
                self.assertEqual(
                    self.run_example(example_path),
                    example_output
                )

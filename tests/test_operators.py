from operator import add, mul
from unittest import TestCase

from ouroboros.operators import Precedence, OperatorType, Operator, BinaryOperator


class TestOperators(TestCase):
    str_op = Operator(OperatorType(Precedence(0), consumes_next=True), str)

    inc_op = Operator(OperatorType(Precedence(0), consumes_previous=True), (lambda a: a + 1))

    add_op = BinaryOperator(Precedence(0), add)
    mul_op = BinaryOperator(Precedence(1), mul)

    pipe_op = BinaryOperator(Precedence(-1), (lambda a, b: b(a)))
    cons_op = BinaryOperator(Precedence(-2, right_associative=True), (lambda a, b: [a] + b))

    def test_basic_folding(self):
        self.assertEqual(
            Operator.reduce([self.str_op, 1]),
            "1"
        )

    def test_postfix_operator(self):
        self.assertEqual(
            Operator.reduce([1, self.inc_op]),
            2
        )

        self.assertEqual(
            Operator.reduce([1, self.inc_op, self.inc_op]),
            3
        )

    def test_binary_operator_basic(self):
        self.assertEqual(
            Operator.reduce([1, self.add_op, 2]),
            3
        )

    def test_binary_operator_chain(self):
        self.assertEqual(
            Operator.reduce([1, self.add_op, 2, self.add_op, 3]),
            6
        )

        self.assertEqual(
            Operator.reduce([1, self.add_op, 1, self.add_op, 1, self.add_op, 1, self.add_op, 1]),
            5
        )

    def test_binary_operator_precedence(self):
        self.assertEqual(
            Operator.reduce([1, self.add_op, 2, self.mul_op, 3]),
            7
        )

        self.assertEqual(
            Operator.reduce([1, self.mul_op, 2, self.add_op, 3]),
            5
        )

    def test_binary_operator_left_associative(self):
        self.assertEqual(
            Operator.reduce([1.0, self.pipe_op, str]),
            "1.0"
        )

        self.assertEqual(
            Operator.reduce([1.0, self.pipe_op, int, self.pipe_op, str]),
            "1"
        )

    def test_binary_operator_right_associative(self):
        with self.assertRaises(TypeError):
            Operator.reduce([1, self.cons_op, 2])

        self.assertEqual(
            Operator.reduce([1, self.cons_op, 2, self.cons_op, []]),
            [1, 2]
        )

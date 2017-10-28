from operator import add, sub, mul, truediv
from random import randrange
from unittest import TestCase

from ouroboros import ouroboros_eval


class TestBasicArithmetic(TestCase):
    ops = {
        "+": add,
        "-": sub,
        "*": mul,
        "/": truediv
    }

    def test_ops(self):
        for op_symbol, op in self.ops.items():
            for _ in range(10):
                x = randrange(0, 10 ** 6)
                y = randrange(0, 10 ** 6)
                with self.subTest(op=op, x=x, y=y):
                    self.assertEqual(
                        ouroboros_eval("{} {} {}".format(x, op_symbol, y)),
                        op(x, y)
                    )

    def test_precedence(self):
        self.assertEqual(ouroboros_eval("1 + 2 * 3"), 7)
        self.assertEqual(ouroboros_eval("3 * 2 + 1"), 7)

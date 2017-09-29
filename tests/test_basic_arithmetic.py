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
                        ouroboros_eval("{} {} {}".format(op_symbol, x, y)),
                        op(x, y)
                    )

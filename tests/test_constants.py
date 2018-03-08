from random import choice, randrange
from string import ascii_letters
from unittest import TestCase

from ouroboros import ouroboros_eval
from ouroboros.internal_types import ListType


class TestConstants(TestCase):
    def test_integer(self):
        for _ in range(10):
            i = randrange(0, 10 ** 6)
            with self.subTest(i=i):
                self.assertEqual(ouroboros_eval(str(i)), i)

    def test_string(self):
        for _ in range(10):
            s = "".join(choice(ascii_letters) for _ in range(randrange(0, 100)))
            with self.subTest(s=s):
                self.assertEqual(ouroboros_eval('"{}"'.format(s)), s)

    def test_list(self):
        result = ouroboros_eval('[1, 2, 3]')
        self.assertIsInstance(result, ListType)
        self.assertEqual(result.list, [1, 2, 3])

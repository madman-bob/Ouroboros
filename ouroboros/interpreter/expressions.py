from toolz import curry

from ordering import Ordering

from ouroboros.parser.operators import OperatorType, Precedence

from ouroboros.utils import cached_class_property

operator_ordering = Ordering()


class Expression:
    right_associative = False

    @cached_class_property
    def precedence(cls):
        if cls is Expression:
            raise NotImplementedError()
        return Precedence(operator_ordering[cls], right_associative=cls.right_associative)

    consumes_previous = False
    consumes_next = False

    def get_operator_type(self):
        return OperatorType(
            self.precedence,
            consumes_previous=self.consumes_previous,
            consumes_next=self.consumes_next
        )

    def __call__(self, *args, **kwargs):
        raise NotImplementedError()


class FunctionExpression(Expression):
    consumes_next = True

    def __init__(self, func):
        self.func = func

    def __call__(self, *args, **kwargs):
        return self.func(*args, **kwargs)


operator_ordering.insert_start(FunctionExpression)


class PrefixExpression(FunctionExpression):
    right_associative = True


operator_ordering.insert_before(FunctionExpression, PrefixExpression)


class BinaryExpression(Expression):
    consumes_previous = True
    consumes_next = True

    def __init__(self, func, precedence=None):
        self.func = func
        self.precedence = precedence or Precedence(operator_ordering[BinaryExpression])

    @curry
    def insert_before(self, func, right_associative=False):
        return BinaryExpression(func, self.precedence.create_before(right_associative=right_associative))

    @curry
    def insert_after(self, func, right_associative=False):
        return BinaryExpression(func, self.precedence.create_after(right_associative=right_associative))

    def insert_equiv(self, func):
        return BinaryExpression(func, self.precedence)

    def __call__(self, *args, **kwargs):
        return self.func(*args, **kwargs)


operator_ordering.insert_before(FunctionExpression, BinaryExpression)

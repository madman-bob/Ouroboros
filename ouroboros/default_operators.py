from functools import wraps

from toolz import curry

from ouroboros.operators import Precedence
from ouroboros.expressions import operator_ordering, Expression


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
        precedence = Precedence(self.precedence.label.insert_before(object()), right_associative=right_associative)
        return BinaryExpression(func, precedence)

    @curry
    def insert_after(self, func, right_associative=False):
        precedence = Precedence(self.precedence.label.insert_after(object()), right_associative=right_associative)
        return BinaryExpression(func, precedence)

    def insert_equiv(self, func):
        return BinaryExpression(self.ouroboros_bin_op_from_python_bin_op(func), self.precedence)

    @classmethod
    def ouroboros_bin_op_from_python_bin_op(cls, func):
        from ouroboros.eval_sentence import eval_semantic_token

        @wraps(func)
        @curry
        def bin_op(left_expression, right_expression):
            return func(eval_semantic_token(left_expression), eval_semantic_token(right_expression))

        return bin_op

    def __call__(self, *args, **kwargs):
        return self.func(*args, **kwargs)


operator_ordering.insert_before(FunctionExpression, BinaryExpression)

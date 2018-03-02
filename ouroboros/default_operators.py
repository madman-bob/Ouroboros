from functools import wraps

from toolz import curry

from ouroboros.sentences import Sentence, Identifier, eval_sentence
from ouroboros.scope import Scope
from ouroboros.operators import Precedence
from ouroboros.expressions import operator_ordering, Expression, eval_expression


class ConstantExpression(Expression):
    def __init__(self, sentence: Sentence, scope: Scope):
        self.sentence = sentence
        self.scope = scope

    def __call__(self):
        return eval_sentence(self.sentence, self.scope)


operator_ordering.insert_start(ConstantExpression)


class Variable(Expression):
    def __init__(self, sentence: Sentence, scope: Scope, precedence=None):
        self.identifier = sentence
        self.scope = scope
        self.precedence = precedence or Precedence(operator_ordering[ConstantExpression])

    def __call__(self):
        return self.scope[self.identifier]


class FunctionExpression(Expression):
    consumes_next = True

    def __init__(self, block, scope: Scope, arg_name: Identifier = None):
        self.block = block
        self.scope = scope
        self.arg_name = arg_name

    @classmethod
    def from_python_function(cls, func):
        return cls(func, {}, Identifier(''))

    def __call__(self, *args, return_scope=False):
        from ouroboros.contexts import BlockContext

        if not args:
            return self

        arg = args[0]

        inner_scope = Scope(parent_scope=self.scope)

        if self.arg_name:
            inner_scope.define(self.arg_name, eval_expression(arg))

        if isinstance(self.block, (ConstantExpression, Variable, FunctionExpression)):
            self.block.scope = inner_scope

        if isinstance(self.block, BlockContext):
            value = eval_sentence(self.block, inner_scope).block(())
        elif isinstance(self.block, Expression):
            value = eval_expression(self.block)
        elif isinstance(self.block, Sentence):
            value = eval_sentence(self.block, inner_scope)
        else:
            value = self.block(arg)

        if return_scope:
            return inner_scope

        if callable(value) and not isinstance(value, Expression):
            return FunctionExpression.from_python_function(value)

        return value

    def __repr__(self):
        return "{}({!r}, {!r}, {!r})".format(self.__class__.__name__, self.block, self.scope, self.arg_name)


operator_ordering.insert_after(ConstantExpression, FunctionExpression)


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
        @wraps(func)
        def bin_op(left_expression, right_expression):
            return func(eval_expression(left_expression), eval_expression(right_expression))

        return bin_op

    def __call__(self, *args, **kwargs):
        value = self.func(*args, **kwargs)

        if callable(value) and not isinstance(value, Expression):
            return FunctionExpression.from_python_function(value)

        return value


operator_ordering.insert_before(FunctionExpression, BinaryExpression)

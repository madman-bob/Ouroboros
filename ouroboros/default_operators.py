from functools import wraps

from toolz import curry

from ordering import Ordering

from ouroboros.sentences import Sentence, Identifier
from ouroboros.scope import Scope
from ouroboros.operators import Precedence
from ouroboros.expressions import Expression

operator_ordering = Ordering()


class ConstantExpression(Expression):
    def __init__(self, sentence: Sentence, scope: Scope):
        self.sentence = sentence
        self.scope = scope

        super().__init__(Precedence(operator_ordering[ConstantExpression]), lambda: self.sentence.eval(self.scope))


operator_ordering.insert_start(ConstantExpression)


class Variable(Expression):
    def __init__(self, sentence: Sentence, scope: Scope, precedence=None):
        self.identifier = sentence
        self.scope = scope

        super().__init__(precedence or Precedence(operator_ordering[ConstantExpression]), lambda: self.scope[sentence])


class FunctionExpression(Expression):
    def __init__(self, block, scope: Scope, arg_name: Identifier = None):
        self.block = block
        self.scope = scope
        self.arg_name = arg_name

        super().__init__(Precedence(operator_ordering[FunctionExpression]), self.__call__, consumes_next=True)

    @classmethod
    def from_python_function(cls, func):
        return cls(func, {}, Identifier(''))

    def eval(self):
        return self

    def __call__(self, arg):
        from ouroboros.contexts import BlockContext

        inner_scope = Scope(parent_scope=self.scope)

        if self.arg_name:
            inner_scope.define(self.arg_name, arg.eval() if isinstance(arg, Expression) else arg)

        if isinstance(self.block, (ConstantExpression, Variable, FunctionExpression)):
            self.block.scope = inner_scope

        if isinstance(self.block, BlockContext):
            value = self.block.eval(inner_scope).block(())
        elif isinstance(self.block, Expression):
            value = self.block.eval()
        elif isinstance(self.block, Sentence):
            value = self.block.eval(inner_scope)
        else:
            value = self.block(arg)

        if callable(value) and not isinstance(value, Expression):
            return FunctionExpression.from_python_function(value)

        return value

    def __repr__(self):
        return "{}({!r}, {!r}, {!r})".format(self.__class__.__name__, self.block, self.scope, self.arg_name)


operator_ordering.insert_after(ConstantExpression, FunctionExpression)


class BinaryExpression(Expression):
    def __init__(self, func, precedence=None):
        super().__init__(precedence or Precedence(operator_ordering[BinaryExpression]), func, consumes_previous=True, consumes_next=True)

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
            left_value = left_expression.eval() if isinstance(left_expression, Expression) else left_expression
            right_value = right_expression.eval() if isinstance(right_expression, Expression) else right_expression
            return func(left_value, right_value)

        return bin_op

    def __call__(self, *args, **kwargs):
        value = self.func(*args, **kwargs)

        if callable(value) and not isinstance(value, Expression):
            return FunctionExpression.from_python_function(value)

        return value


operator_ordering.insert_before(FunctionExpression, BinaryExpression)

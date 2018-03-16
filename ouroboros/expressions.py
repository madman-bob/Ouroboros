from ordering import Ordering

from ouroboros.operators import Operator, OperatorType, Precedence

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

    def get_operator(self):
        def func(*args, get_expression=False):
            if get_expression:
                return self
            return try_get_operator(self(*(unwrap_operator(arg) for arg in args)))

        return Operator(
            OperatorType(
                self.precedence,
                consumes_previous=self.consumes_previous,
                consumes_next=self.consumes_next
            ),
            func
        )

    def __call__(self, *args, **kwargs):
        raise NotImplementedError()


def try_get_operator(obj: object) -> object:
    if isinstance(obj, Expression):
        return obj.get_operator()
    return obj


def unwrap_operator(operator: object) -> object:
    if isinstance(operator, Operator):
        return operator(get_expression=True)
    return operator


def eval_expression(expression: object) -> object:
    if isinstance(expression, Expression):
        return expression.get_operator()()
    if isinstance(expression, Operator):
        return expression()
    return expression

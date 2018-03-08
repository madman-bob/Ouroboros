from functools import reduce

from toolz import curry

from ouroboros.default_operators import FunctionExpression
from ouroboros.expressions import eval_expression
from ouroboros.sentences import Identifier


class ReturnType:
    def __init__(self, return_value):
        self.return_value = return_value


class ObjectType:
    def __init__(self, attributes):
        self.attributes = attributes

    def __str__(self):
        return str(self.attributes)


class ListType(ObjectType):
    def __init__(self, values):
        self.list = list(values)

        @FunctionExpression.from_python_function
        def ou_append(item):
            self.list.append(eval_expression(item))

        @FunctionExpression.from_python_function
        def ou_map(func):
            return ListType(map(eval_expression(func), self.list))

        @FunctionExpression.from_python_function
        def ou_filter(func):
            return ListType(filter(eval_expression(func), self.list))

        @FunctionExpression.from_python_function
        @curry
        def ou_reduce(func, initial):
            func = eval_expression(func)
            return reduce(
                lambda x, y: func(x)(y),
                self.list,
                eval_expression(initial)
            )

        super().__init__({
            Identifier("append"): ou_append,
            Identifier("map"): ou_map,
            Identifier("filter"): ou_filter,
            Identifier("reduce"): ou_reduce
        })

    def __add__(self, other):
        assert isinstance(other, ListType)
        return ListType(self.list + other.list)

    def __str__(self):
        return str(self.list)

    def __repr__(self):
        return repr(self.list)

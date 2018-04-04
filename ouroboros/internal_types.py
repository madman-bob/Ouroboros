from functools import reduce

from toolz import curry

from ouroboros.scope import Scope
from ouroboros.default_operators import FunctionExpression
from ouroboros.lexer.lexical_tokens import Identifier
from ouroboros.utils import cached_class_property, cached_property


class ReturnType:
    def __init__(self, return_value):
        self.return_value = return_value


class ObjectType:
    class_attributes = cached_class_property(lambda cls: Scope())

    @cached_property
    class bound_class_attributes:
        def __init__(self, instance):
            self.instance = instance

        def __getitem__(self, item):
            return self.instance.class_attributes[item](self.instance)

        def __contains__(self, item):
            return item in self.instance.class_attributes

    def __init__(self, attributes):
        self.attributes = Scope(attributes, self.bound_class_attributes)

    def __str__(self):
        return str(self.attributes)


class ListType(ObjectType):
    def __init__(self, values):
        self.list = list(values)

        @FunctionExpression
        def ou_append(item):
            from ouroboros.eval_sentence import eval_semantic_token
            self.list.append(eval_semantic_token(item))

        @FunctionExpression
        def ou_map(func):
            from ouroboros.eval_sentence import eval_semantic_token
            return ListType(map(eval_semantic_token(func), self.list))

        @FunctionExpression
        def ou_filter(func):
            from ouroboros.eval_sentence import eval_semantic_token
            return ListType(filter(eval_semantic_token(func), self.list))

        @FunctionExpression
        @curry
        def ou_reduce(func, initial):
            from ouroboros.eval_sentence import eval_semantic_token
            func = eval_semantic_token(func)
            return reduce(
                lambda x, y: func(x)(y),
                self.list,
                eval_semantic_token(initial)
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

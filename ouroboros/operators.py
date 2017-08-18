from functools import total_ordering


@total_ordering
class Precedence:
    def __init__(self, label, right_associative=False):
        self.label = label
        self.right_associative = right_associative

    def __lt__(self, other):
        if not isinstance(other, Precedence):
            raise TypeError
        return self.label < other.label

    def __eq__(self, other):
        return type(self) is type(other) and self.label == other.label


class Operator:
    def __init__(self, precedence, func, consumes_previous=False, consumes_next=False):
        self.precedence = precedence
        self.func = func
        self.consumes_previous = consumes_previous
        self.consumes_next = consumes_next

    def __call__(self, *args, **kwargs):
        return self.func(*args, **kwargs)

    @classmethod
    def reduce(cls, op_list):
        while len(op_list) > 1:
            i_max, op_max = cls.find_max_precedence(op_list)

            args = []
            if op_max.consumes_previous:
                args.append(op_list[i_max - 1])
            if op_max.consumes_next:
                args.append(op_list[i_max + 1])

            op_list[i_max - op_max.consumes_previous:i_max + 1 + op_max.consumes_next] = [op_max(*args)]

        return op_list[0]

    @classmethod
    def find_max_precedence(cls, iterable):
        i_max, op_max = None, None
        for i, op in enumerate(iterable):
            if not isinstance(op, Operator):
                continue

            if i_max is None or op.precedence > op_max.precedence or op.precedence == op_max.precedence and op.precedence.right_associative:
                i_max, op_max = i, op

        return i_max, op_max


class BinaryOperator(Operator):
    def __init__(self, precedence, func):
        super().__init__(precedence, func, consumes_previous=True, consumes_next=True)

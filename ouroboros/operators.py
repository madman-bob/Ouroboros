from dataclasses import dataclass
from functools import total_ordering
from typing import Callable

from ordering import OrderingItem


@total_ordering
@dataclass(frozen=True)
class Precedence:
    label: OrderingItem
    right_associative: bool = False

    def __lt__(self, other):
        if not isinstance(other, Precedence):
            raise TypeError
        return self.label < other.label

    def create_before(self, label=None, right_associative=False):
        if label is None:
            label = object()

        return Precedence(self.label.insert_before(label), right_associative=right_associative)

    def create_after(self, label=None, right_associative=False):
        if label is None:
            label = object()

        return Precedence(self.label.insert_after(label), right_associative=right_associative)


@total_ordering
@dataclass(frozen=True)
class OperatorType:
    precedence: Precedence
    consumes_previous: bool = False
    consumes_next: bool = False

    def __lt__(self, other):
        if not isinstance(other, OperatorType):
            raise TypeError
        return self.precedence < other.precedence


@dataclass(frozen=True)
class Operator:
    operator_type: OperatorType
    func: Callable

    @property
    def precedence(self):
        return self.operator_type.precedence

    @property
    def consumes_previous(self):
        return self.operator_type.consumes_previous

    @property
    def consumes_next(self):
        return self.operator_type.consumes_next

    def __call__(self, *args, **kwargs):
        return self.func(*args, **kwargs)

    @classmethod
    def reduce(cls, op_list):
        while True:
            i_max, op_max = cls.find_max_precedence(op_list)

            if i_max is None:
                break

            args = []
            if op_max.consumes_previous:
                args.append(op_list[i_max - 1])
            if op_max.consumes_next:
                args.append(op_list[i_max + 1])

            op_list[i_max - op_max.consumes_previous:i_max + 1 + op_max.consumes_next] = [op_max(*args)]

        assert len(op_list) == 1

        return op_list[0]

    @classmethod
    def find_max_precedence(cls, iterable):
        i_max, op_max = None, None
        for i, op in enumerate(iterable):
            if not isinstance(op, Operator):
                continue

            if i == 0 and op.consumes_previous:
                continue

            if i == len(iterable) - 1 and op.consumes_next:
                continue

            if op.consumes_next and i < len(iterable) - 1 and isinstance(iterable[i + 1], Operator) and iterable[i + 1].consumes_previous:
                continue

            if i_max is None or op.precedence > op_max.precedence or op.precedence == op_max.precedence and op.precedence.right_associative:
                i_max, op_max = i, op

        return i_max, op_max

    def __repr__(self):
        return "{}({!r}, {}, {}, {})".format(self.__class__.__name__, self.precedence, self.func, self.consumes_previous, self.consumes_next)


@dataclass(frozen=True)
class BinaryOperator(Operator):
    def __init__(self, precedence, func):
        super().__init__(OperatorType(precedence, consumes_previous=True, consumes_next=True), func)

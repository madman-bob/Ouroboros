from ordering import Ordering

from ouroboros.operators import OperatorType, Precedence

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

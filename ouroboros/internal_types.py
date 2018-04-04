from ouroboros.scope import Scope
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

        super().__init__({})

    def __add__(self, other):
        assert isinstance(other, ListType)
        return ListType(self.list + other.list)

    def __str__(self):
        return str(self.list)

    def __repr__(self):
        return repr(self.list)

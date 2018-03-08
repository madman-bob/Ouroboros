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

        super().__init__({})

    def __add__(self, other):
        assert isinstance(other, ListType)
        return ListType(self.list + other.list)

    def __str__(self):
        return str(self.list)

    def __repr__(self):
        return repr(self.list)

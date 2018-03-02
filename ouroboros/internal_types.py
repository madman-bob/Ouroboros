class ReturnType:
    def __init__(self, return_value):
        self.return_value = return_value


class ObjectType:
    def __init__(self, attributes):
        self.attributes = attributes

    def __str__(self):
        return str(self.attributes)

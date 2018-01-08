class cached_class_property(object):
    def __init__(self, func):
        self.func = func

    def __get__(self, obj, cls):
        value = self.func(cls)
        setattr(cls, self.func.__name__, value)
        return value

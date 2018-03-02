from toolz import memoize


class cached_class_property(object):
    def __init__(self, func):
        self.func = memoize(func)

    def __get__(self, obj, cls):
        return self.func(cls)

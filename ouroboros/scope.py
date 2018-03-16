from typing import TypeVar, MutableMapping

T = TypeVar('T')
S = TypeVar('S')


class Scope(MutableMapping[T, S]):
    def __init__(self, local_scope=None, parent_scope=None):
        self._local_scope = local_scope if local_scope is not None else {}
        self._parent_scope = parent_scope if parent_scope is not None else {}

    def define(self, key, value):
        if key in self._local_scope or key in self._parent_scope:
            raise KeyError("Variable {} has already been defined".format(key))
        self._local_scope[key] = value

    def __getitem__(self, key):
        if key in self._local_scope:
            return self._local_scope[key]
        elif key in self._parent_scope:
            return self._parent_scope[key]
        else:
            raise KeyError("Variable {} has not been defined".format(key))

    def __setitem__(self, key, value):
        if key in self._local_scope:
            self._local_scope[key] = value
        elif key in self._parent_scope:
            self._parent_scope[key] = value
        else:
            raise KeyError("Variable {} has not been defined".format(key))

    def __delitem__(self, key):
        if key in self._local_scope:
            del self._local_scope[key]
        elif key in self._parent_scope:
            del self._parent_scope[key]
        else:
            raise KeyError("Variable {} has not been defined".format(key))

    def __iter__(self):
        yield from self._local_scope
        yield from self._parent_scope

    def __len__(self):
        return len(self._local_scope) + len(self._parent_scope)

    def __contains__(self, key):
        return key in self._local_scope or key in self._parent_scope

    def __repr__(self):
        return "{}({}, {})".format(self.__class__.__name__, self._local_scope, self._parent_scope)

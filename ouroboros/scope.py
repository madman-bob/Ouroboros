from dataclasses import dataclass, field
from typing import TypeVar, MutableMapping

T = TypeVar('T')
S = TypeVar('S')


@dataclass
class Scope(MutableMapping[T, S]):
    local_scope: MutableMapping[T, S] = field(default_factory=dict)
    parent_scope: MutableMapping[T, S] = field(default_factory=dict)

    def define(self, key, value):
        if key in self.local_scope or key in self.parent_scope:
            raise KeyError("Variable {} has already been defined".format(key))
        self.local_scope[key] = value

    def __getitem__(self, key):
        if key in self.local_scope:
            return self.local_scope[key]
        elif key in self.parent_scope:
            return self.parent_scope[key]
        else:
            raise KeyError("Variable {} has not been defined".format(key))

    def __setitem__(self, key, value):
        if key in self.local_scope:
            self.local_scope[key] = value
        elif key in self.parent_scope:
            self.parent_scope[key] = value
        else:
            raise KeyError("Variable {} has not been defined".format(key))

    def __delitem__(self, key):
        if key in self.local_scope:
            del self.local_scope[key]
        elif key in self.parent_scope:
            del self.parent_scope[key]
        else:
            raise KeyError("Variable {} has not been defined".format(key))

    def __iter__(self):
        yield from self.local_scope
        yield from self.parent_scope

    def __len__(self):
        return len(self.local_scope) + len(self.parent_scope)

    def __contains__(self, key):
        return key in self.local_scope or key in self.parent_scope

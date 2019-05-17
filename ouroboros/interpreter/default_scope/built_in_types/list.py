from functools import reduce

from toolz import curry

from ouroboros.interpreter.internal_types import ListType
from ouroboros.interpreter.eval_sentence import SemanticToken, eval_semantic_token
from ouroboros.interpreter.default_scope.built_in_types.base import class_attribute

__all__ = ("ou_append", "ou_map", "ou_filter", "ou_reduce")


@class_attribute(ListType, "append")
@curry
def ou_append(self: ListType, item: SemanticToken):
    self.list.append(eval_semantic_token(item))


@class_attribute(ListType, "map")
@curry
def ou_map(self: ListType, func: SemanticToken):
    return ListType(map(eval_semantic_token(func), self.list))


@class_attribute(ListType, "filter")
@curry
def ou_filter(self: ListType, func: SemanticToken):
    return ListType(filter(eval_semantic_token(func), self.list))


@class_attribute(ListType, "reduce")
@curry
def ou_reduce(self: ListType, func: SemanticToken, initial: SemanticToken):
    func = eval_semantic_token(func)
    return reduce(
        lambda x, y: func(x)(y),
        self.list,
        eval_semantic_token(initial)
    )

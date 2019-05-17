from toolz import curry

from ouroboros.lexer.lexical_tokens import Identifier

__all__ = ("class_attribute",)


@curry
def class_attribute(object_type, attribute_name, value):
    object_type.class_attributes.define(Identifier(attribute_name), value)
    return value

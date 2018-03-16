from namedlist import namedtuple

Statement = namedtuple('Statement', ['terms'])

Block = namedtuple('Block', ['statements'])

ListStatement = namedtuple('ListStatement', ['values'])

Comment = namedtuple('Comment', ['comment_text'])

StringStatement = namedtuple('StringStatement', ['value'])

ImportStatement = namedtuple('ImportStatement', ['path'])

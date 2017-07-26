import sys

import argparse

from ouroboros.contexts import BlockContext
from ouroboros.scope import Scope
from ouroboros.default_scope import default_scope

parser = argparse.ArgumentParser()
parser.add_argument('file', nargs='?', type=argparse.FileType('r'), default=sys.stdin)
args = parser.parse_args()

with args.file as input_file:
    context = BlockContext(input_file.read())

context.eval(default_scope)(Scope(), ())

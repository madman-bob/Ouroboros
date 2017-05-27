import sys

import argparse

from contexts import BlockContext
from scope import Scope
from default_scope import default_scope

parser = argparse.ArgumentParser()
parser.add_argument('file', nargs='?', type=argparse.FileType('r'), default=sys.stdin)
args = parser.parse_args()

with args.file as input_file:
    context = BlockContext(input_file.read())

context.eval(default_scope)(Scope(), ())

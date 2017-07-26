import sys

import argparse

from ouroboros import ouroboros_exec

parser = argparse.ArgumentParser()
parser.add_argument('file', nargs='?', type=argparse.FileType('r'), default=sys.stdin)
args = parser.parse_args()

with args.file as input_file:
    ouroboros_exec(input_file.read())

from .args import argument_parser
from .run import run

import sys

def main(args=sys.argv[1:]):
    options = argument_parser().parse_args(args)
    run(options)

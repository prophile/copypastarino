from __future__ import print_function

from .pasta import Pasta

def run(args):
    pasta = Pasta(args.project,
                  library=args.library,
                  python2=args.python2,
                  tests=args.tests)
    pasta.setup()

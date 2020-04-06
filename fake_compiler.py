#!/usr/bin/env python3

import argparse
import os
import sys

from contextlib import contextmanager
from typing import ContextManager


@contextmanager
def with_fake_compiler() -> ContextManager[None]:
    cc = os.getenv('CC', os.getenv('CXX', 'cc'))
    fake = os.path.abspath(__file__)
    from conans import tools
    with tools.environment_append({'ORIGINAL_CC': cc, 'CC': fake, 'CXX': fake}):
        yield


def _main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument('-o', dest='output')
    args, _ = parser.parse_known_args()

    if args.output is None:
        cc = os.getenv('ORIGINAL_CC')
        os.execvp(cc, [cc] + sys.argv[1:])
    else:
        os.symlink('/bin/true', args.output)


if __name__ == '__main__':
    _main()

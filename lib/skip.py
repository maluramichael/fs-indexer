import os
from pathlib import PurePath

from lib.args import args


def skip_dir(path):
    exclude_dir = args.exclude_dir
    exclude_hidden_dirs = args.exclude_hidden_dirs

    if exclude_hidden_dirs and os.path.basename(path).startswith('.'):
        return True

    if exclude_dir and path in exclude_dir:
        return True

    return False


def skip_file(file, path):
    exclude_file = args.exclude_file

    for exclude in exclude_file:
        if PurePath(file).match(exclude):
            return True

    return False

import os
from typing import Iterator

from lib.meta import create_base_meta_data
from lib.path import Path
from lib.rewrite import Rewrite
from lib.scanner_args import args
from lib.skip import skip_dir, skip_file


def walk_filesystem() -> Iterator[dict]:
    starting_path = args.path
    rewrite_path = args.rewrite
    parse_dirs = not args.only_files or args.only_dirs
    parse_files = not args.only_dirs or args.only_files
    rewriter = Rewrite(starting_path, rewrite_path)

    for root, dirs, files in os.walk(starting_path):
        if skip_dir(root):
            continue

        # if parse_dirs:
        #     sorted_dirs = sorted(dirs)
        #     for directory in sorted_dirs:
        #         dir_path = os.path.join(root, directory)
        #         rewritten_path = dir_path
        #
        #         if rewrite_path:
        #             rewritten_path = dir_path.replace(starting_path, rewrite_path)
        #
        #         if skip_dir(rewritten_path):
        #             continue
        #
        #         print(f'Parsing directory: {dir_path}')
        #         meta_data = create_base_meta_data(dir_path)
        #         meta_data['name'] = directory
        #         meta_data['path'] = rewritten_path
        #         meta_data['original_path'] = dir_path
        #
        #         yield meta_data

        if parse_files:
            sorted_files = sorted(files)

            for file in sorted_files:
                file_path = Path(root, file, rewriter)

                if skip_file(file, file_path):
                    continue

                meta_data = create_base_meta_data(file_path)

                if meta_data is None:
                    continue

                meta_data['name'] = file
                meta_data['path'] = file_path
                meta_data['folder_path'] = root

                yield meta_data

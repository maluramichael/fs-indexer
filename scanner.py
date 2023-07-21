import os
import sys
from typing import Iterator

from lib.args import args
from lib.meta import create_base_meta_data
from lib.parser import all_type_content_map, type_content_map, parse_content
from lib.skip import skip_dir, skip_file


def walk_filesystem() -> Iterator[dict]:
    path = args.path
    rewrite = args.rewrite
    parse_dirs = not args.only_files or args.only_dirs
    parse_files = not args.only_dirs or args.only_files

    for root, dirs, files in os.walk(path):
        if skip_dir(root):
            continue

        if parse_dirs:
            sorted_dirs = sorted(dirs)
            for directory in sorted_dirs:
                dir_path = os.path.join(root, directory)
                rewritten_path = dir_path

                if rewrite:
                    rewritten_path = dir_path.replace(path, rewrite)

                if skip_dir(rewritten_path):
                    continue

                print(f'Parsing directory: {dir_path}')
                meta_data = create_base_meta_data(dir_path)
                meta_data['name'] = directory
                meta_data['path'] = rewritten_path
                meta_data['original_path'] = dir_path

                yield meta_data

        if parse_files:
            sorted_files = sorted(files)

            for file in sorted_files:
                file_path = os.path.join(root, file)
                rewritten_path = file_path

                if rewrite:
                    rewritten_path = file_path.replace(path, rewrite)

                if skip_file(file, rewritten_path):
                    continue

                print(f'Parsing file: {file_path}')
                meta_data = create_base_meta_data(file_path)

                if meta_data is None:
                    continue

                meta_data['name'] = file
                meta_data['path'] = rewritten_path
                meta_data['original_path'] = file_path

                yield meta_data


def main():
    if not os.path.exists(args.path):
        print("The path provided does not exist")
        sys.exit(1)

    if not os.path.exists(args.thumbnail_path):
        os.makedirs(args.thumbnail_path)

    if args.include_type is None:
        args.include_type = list(all_type_content_map.keys())

    for included_type in args.include_type:
        if included_type not in all_type_content_map:
            print(f'Unknown type: {included_type}')
            sys.exit(1)

        type_content_map[included_type] = all_type_content_map[included_type]

    for meta_data in walk_filesystem():
        print(f"Found: {meta_data['path']}")

        # process meta data further
        meta_data = parse_content(meta_data)

        # save meta data to database


if __name__ == '__main__':
    main()

import datetime
import mimetypes
import os

from lib.cache import FileCache
from lib.path import Path


def get_meta_for_directory(path):
    # exclude_file = []
    #
    # if args is not None and args.exclude_file is not None:
    #     exclude_file = args.exclude_file
    #
    # content = os.listdir(path)
    #
    # for exclude in exclude_file:
    #     content = [f for f in content if not PurePath(f).match(exclude)]

    return {
        'type': 'dir',
        # 'content': content,
    }


def get_meta_for_image(path):
    return {
        'type': 'image',
    }


def get_meta_for_video(path):
    return {
        'type': 'video',
    }


type_meta_map = {
    'dir': get_meta_for_directory,
    'image': get_meta_for_image,
    'video': get_meta_for_video,
}


@FileCache.memoize(expire=120)
def get_type(path: Path, fast=True):
    original_path = path.original_path()

    if os.path.isfile(original_path):
        if fast:
            extension = os.path.splitext(original_path)[1]

            if extension == '.jpg' or extension == '.png':
                return 'image'

            if extension == '.mp4':
                return 'video'
        else:
            return mimetypes.guess_type(original_path)
    elif os.path.isdir(original_path):
        return 'dir'

    return None


@FileCache.memoize(expire=120)
def create_base_meta_data(path: Path):
    type_of_path = get_type(path)

    if type_of_path is None:
        return None

    if type_of_path not in type_meta_map:
        raise Exception(f'No parser for type: {type_of_path}')

    meta_data = type_meta_map[type_of_path](path)
    mtime = os.path.getmtime(path.original_path())
    stat = os.stat(path.original_path())
    meta_data['mtime'] = datetime.datetime.fromtimestamp(mtime)
    meta_data['size'] = stat.st_size

    return meta_data

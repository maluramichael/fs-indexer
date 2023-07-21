import mimetypes
import os

from lib.cache import FileCache


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
def get_type(path, fast=True):
    if os.path.isfile(path):
        if fast:
            extension = os.path.splitext(path)[1]

            if extension == '.jpg' or extension == '.png':
                return 'image'

            if extension == '.mp4':
                return 'video'
        else:
            return mimetypes.guess_type(path)
    elif os.path.isdir(path):
        return 'dir'

    return None


@FileCache.memoize(expire=120)
def create_base_meta_data(path):
    type_of_path = get_type(path)

    if type_of_path is None:
        return None

    if type_of_path not in type_meta_map:
        raise Exception(f'No parser for type: {type_of_path}')

    return type_meta_map[type_of_path](path)

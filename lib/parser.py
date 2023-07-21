import os

from lib.args import args
from lib.thumbnail import generate_thumbnail_path, generate_image_thumbnail, generate_video_thumbnail


def parse_content_image(meta_data):
    thumbnail_path = generate_thumbnail_path(meta_data)
    size = args.thumbnail_size

    if thumbnail_path and not os.path.isfile(thumbnail_path):
        success = generate_image_thumbnail(meta_data['original_path'], thumbnail_path, size)

        if success:
            meta_data['thumbnail_path'] = thumbnail_path
        else:
            meta_data['thumbnail_path'] = None

    return meta_data


def parse_content_video(meta_data):
    thumbnail_path = generate_thumbnail_path(meta_data)

    if thumbnail_path and not os.path.isfile(thumbnail_path):
        success = generate_video_thumbnail(meta_data['original_path'], thumbnail_path)

        if success:
            meta_data['thumbnail_path'] = thumbnail_path
        else:
            meta_data['thumbnail_path'] = None

    return meta_data


all_type_content_map = {
    'image': parse_content_image,
    'video': parse_content_video,
}
type_content_map = {}


def parse_content(meta_data):
    if meta_data['type'] == 'dir':
        return meta_data

    if meta_data['type'] not in type_content_map:
        return None

    return type_content_map[meta_data['type']](meta_data)

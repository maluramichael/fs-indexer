import os
from PIL import Image as PILImage

from lib.entities import Entry
from lib.rewrite import Rewrite
from lib.scanner_args import args
from lib.thumbnail import generate_thumbnail_path, generate_image_thumbnail, generate_video_thumbnail
from lib.video import get_video_meta_data


def parse_content_image(entity):
    rewriter = Rewrite(args.rewrite, args.path)
    thumbnail_path = generate_thumbnail_path(entity)
    thumbnail_size = args.thumbnail_size
    original_file_path = os.path.join(entity.path, entity.name)
    original_file_path = rewriter.rewrite(original_file_path)

    if thumbnail_path is None:
        raise Exception('Could not generate thumbnail path')

    if not os.path.isfile(thumbnail_path):
        generate_image_thumbnail(original_file_path, thumbnail_path, thumbnail_size)

    try:
        image = PILImage.open(original_file_path)
        entity.width, entity.height = image.size
    except Exception as e:
        print(f'Could not open image {original_file_path}: {e}')
        return None

    return entity


def parse_content_video(entity):
    rewriter = Rewrite(args.rewrite, args.path)
    thumbnail_path = generate_thumbnail_path(entity)
    thumbnail_size = args.thumbnail_size
    original_file_path = os.path.join(entity.path, entity.name)
    original_file_path = rewriter.rewrite(original_file_path)

    if thumbnail_path is None:
        raise Exception('Could not generate thumbnail path')

    if not os.path.isfile(thumbnail_path):
        generate_video_thumbnail(original_file_path, thumbnail_path)

    video_meta_data = get_video_meta_data(original_file_path)

    entity.duration_in_seconds = video_meta_data['duration']
    entity.width = video_meta_data['width']
    entity.height = video_meta_data['height']

    return entity


all_type_content_map = {
    'image': parse_content_image,
    'video': parse_content_video,
}
type_content_map = {}


def parse_content(entry: Entry):
    if entry.type == 'dir':
        return entry

    if entry.type not in type_content_map:
        return None

    return type_content_map[entry.type](entry)

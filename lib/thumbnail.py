import hashlib
import os
import sys

import ffmpeg
from PIL import Image

from lib.args import args


def get_full_thumbnail_path(meta_data):
    thumbnail_path = args.thumbnail_path

    if thumbnail_path is None:
        return meta_data

    path_as_sha1_hash = hashlib.sha1(meta_data['path'].encode('utf-8')).hexdigest()
    dir_parts = path_as_sha1_hash[:2]
    thumbnail_dir = os.path.join(thumbnail_path, dir_parts)
    thumbnail_path = os.path.join(thumbnail_dir, path_as_sha1_hash + '.jpg')

    return thumbnail_path


def generate_thumbnail_path(meta_data):
    full_thumbnail_path = get_full_thumbnail_path(meta_data)
    thumbnail_dir = os.path.dirname(full_thumbnail_path)

    if not os.path.isdir(thumbnail_dir):
        os.makedirs(thumbnail_dir)

    return full_thumbnail_path


def generate_image_thumbnail(path, thumbnail_path, size=(256, 256)):
    try:
        image = Image.open(path)
        image.thumbnail(size)
        image.save(thumbnail_path, 'JPEG')
        return True
    except Exception as e:
        print(f'Could not generate thumbnail for {path}: {e}')
        return False


def generate_video_thumbnail(path, thumbnail_path):
    ffprobe_path = os.path.join(os.path.dirname(args.ffmpeg_path), 'ffprobe')

    try:
        probe = ffmpeg.probe(path, cmd=ffprobe_path)
        video_stream = next((stream for stream in probe['streams'] if stream['codec_type'] == 'video'), None)
        duration = float(video_stream['duration']) // 2
        width = int(video_stream['width'])
        width = min(width, 256)

        (
            ffmpeg
            .input(path, ss=duration)
            .filter('scale', width, -1)
            .output(thumbnail_path, vframes=1)
            .overwrite_output()
            .run(capture_stdout=True, capture_stderr=True, cmd=args.ffmpeg_path)
        )
    except ffmpeg.Error as e:
        print(e.stderr.decode(), file=sys.stderr)
        return False

    return True

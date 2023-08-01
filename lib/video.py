import os
import sys

import ffmpeg

from lib.scanner_args import args


def get_video_meta_data(path):
    ffprobe_path = os.path.join(os.path.dirname(args.ffmpeg_path), 'ffprobe')

    try:
        probe = ffmpeg.probe(path, cmd=ffprobe_path)
        video_stream = next((stream for stream in probe['streams'] if stream['codec_type'] == 'video'), None)
        duration = float(video_stream['duration'])
        return {
            'duration': duration,
            'width': video_stream['width'],
            'height': video_stream['height'],
        }
    except ffmpeg.Error as e:
        print(e.stderr.decode(), file=sys.stderr)
        return False

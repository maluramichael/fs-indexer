import argparse

parser = argparse.ArgumentParser(description='Scan a directory for files')

parser.add_argument('--rewrite', nargs='?', metavar='rewrite', type=str, help='The path to rewrite')
parser.add_argument('--include-type', action='append', metavar='include_type', type=str, help='The types of files to include', default=None)
parser.add_argument('--exclude-dir', action='append', metavar='exclude_dir', type=str, help='The directories to exclude', default=[])
parser.add_argument('--exclude-file', action='append', metavar='exclude_file', type=str, help='The files to exclude', default=[])
parser.add_argument('--exclude-hidden-dirs', action='store_true', help='Exclude hidden directories', default=False)
parser.add_argument('--thumbnail-path', nargs='?', metavar='thumbnail_path', type=str, help='The path to store thumbnails', default='.thumbnails')
parser.add_argument('--thumbnail-size', nargs=2, metavar=('width', 'height'), type=int, help='The size of the thumbnails', default=(256, 256))
parser.add_argument('--ffmpeg-path', nargs='?', metavar='ffmpeg_path', type=str, help='The path to ffmpeg', default='ffmpeg')
parser.add_argument('--pool-size', nargs='?', metavar='pool_size', type=int, help='The size of the thread pool', default=4)

only_group = parser.add_mutually_exclusive_group()
only_group.add_argument('--only-files', action='store_true', help='Only include files', default=False)
only_group.add_argument('--only-dirs', action='store_true', help='Only directories files', default=False)

parser.add_argument('path', metavar='path', type=str, help='The path to scan')

args = parser.parse_args()

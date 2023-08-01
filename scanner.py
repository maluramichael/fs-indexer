import os
import queue
import sys
import threading
import time

from lib.scanner_args import args
from lib.db import flush_bulk, create_db, session
from lib.entities import Directory, Entry, Image, Video
from lib.parser import all_type_content_map, type_content_map, parse_content
from walker import walk_filesystem

job_queue = queue.Queue()


def worker():
    print(f"Starting worker: {threading.current_thread().name}")

    while True:
        meta_data = job_queue.get()

        if meta_data is None:
            break

        print(f"Processing: {meta_data['path']}")
        time.sleep(10)
        job_queue.task_done()


def start_meta_data_workers(pool_size: int):
    threads = []

    for i in range(pool_size):
        thread = threading.Thread(target=worker, name=f"MetaDataWorker-{i}")
        thread.start()
        threads.append(thread)

    return threads


def stop_meta_data_workers(threads):
    for thread in threads:
        job_queue.put(None)
    for thread in threads:
        thread.join()


def walk_and_update_database():
    type_to_model_map = {
        'image': Image,
        'video': Video,
        'audio': None,
        'document': None,
        'archive': None,
        'other': None,
    }

    # run scanner
    # put all files into the database
    for meta_data in walk_filesystem():
        print(f"Processing: {meta_data['path']}")
        directory = session.query(Directory).filter_by(path=meta_data['path'].get_directory()).first()

        if directory is None:
            directory = Directory()
            directory.path = meta_data['path'].get_directory()
            session.add(directory)
            session.commit()

        type = meta_data['type']
        orm_model = type_to_model_map[type]

        if orm_model is None:
            continue

        path = meta_data['path'].get_directory()
        name = meta_data['name']
        entry = session.query(orm_model).filter_by(
            path=path,
            name=name
        ).first()

        if entry is None:
            entry = orm_model()
            entry.path = path
            entry.name = name
            entry.mtime = meta_data['mtime']
            entry.type = meta_data['type']
            entry.size = meta_data['size']

            entry = parse_content(entry)

            session.add(entry)
            session.commit()

        # # meta_data = parse_content(meta_data)
        # job_queue.put(meta_data)
        #
        # if job_queue.qsize() > 100:
        #     print("Waiting for queue to drain")
        #     job_queue.join()
        #     print("Queue drained")
    flush_bulk()


def main():
    # prepare database
    create_db()

    # make sure paths exist
    if not os.path.exists(args.path):
        print("The path provided does not exist")
        sys.exit(1)

    if not os.path.exists(args.thumbnail_path):
        os.makedirs(args.thumbnail_path)

    # prepare type maps
    if args.include_type is None:
        args.include_type = list(all_type_content_map.keys())

    for included_type in args.include_type:
        if included_type not in all_type_content_map:
            print(f'Unknown type: {included_type}')
            sys.exit(1)

        type_content_map[included_type] = all_type_content_map[included_type]

    # prepare worker pool
    # workers = start_meta_data_workers(pool_size=args.pool_size)

    walk_and_update_database()

    # job_queue.join()
    # stop_meta_data_workers(workers)


if __name__ == '__main__':
    main()

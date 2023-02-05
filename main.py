import os
import re
from pathlib import Path

from watchdog.observers import Observer
from watchdog.events import FileSystemEventHandler


from loguru import logger

from ArgsParser import ArgsParser
from Summary import Summary
from utils import handle_resolved_dirs, stopwatch

# CONFIG_PATH = '../config.ini.bak'
CONFIG_PATH = 'config.ini'


@stopwatch
def main():
    logger.info('parse config')
    args_parser = ArgsParser(CONFIG_PATH)
    logger.info('start detection')
    os.system('python yolov5/detect.py ' + ' '.join(args_parser.get_args()))

    logger.info('write summary')
    Summary(
        project_path=Path(args_parser.by_key('project')),
        source_path=Path(args_parser.by_key('source')),
        exp_name=args_parser.by_key('name'),
    ).write_custom_summaries(rm_exp=False)

    handle_resolved_dirs(
        source_path=Path(args_parser.by_key('source'), )
    )
    logger.info('finished')


class FileCreateHandler(FileSystemEventHandler):
    def __init__(self):
        print('Elapsed time: {}'.format(main))

    def on_created(self, event):
        if not re.search("^SO.*dat$", Path(event.src_path).name):
            return
        print('Elapsed time: {}'.format(main))


if __name__ == '__main__':
    logger.info('run file listener')
    observer = Observer()
    observer.schedule(FileCreateHandler(),
                      ArgsParser(CONFIG_PATH).by_key('source'), recursive=True)
    observer.start()
    try:
        while observer.is_alive():
            observer.join(1)
    finally:
        observer.stop()
        observer.join()

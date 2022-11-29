from configparser import ConfigParser
from pathlib import Path
import sched
import os
import sys
import shutil

from loguru import logger

from utils import mkdir_images_from_dat_path, \
    create_summary, move_processed_dat

config = ConfigParser()
config.read('config.ini')


def get_args() -> list[str]:
    args = []

    for key in config['DEFAULT']:

        if key == 'source':
            source_dat = Path(config['DEFAULT'][key])
            err = mkdir_images_from_dat_path(source_dat)
            if err:
                sys.exit(str(err))
            args.append("--{key} {image_path}".format(
                key=key,
                image_path=str(source_dat / 'images'),
            ))
            continue

        if key in ('save-txt', 'save-conf',
                   'save-crop', 'hide-labels', 'hide-conf'):
            if config['DEFAULT'].getboolean(key):
                args.append('--{key}'.format(
                    key=key,
                ))
            continue

        if key in ('timer_sec', 'iter_count'):
            continue

        args.append("--{key} {value}".format(
            key=key,
            value=config['DEFAULT'][key],
        ))
    logger.info('config parsed')
    return args


def main() -> None:
    print('MAIN')
    args = get_args()
    logger.info('start detection')
    os.system('python yolov5/detect.py ' + ' '.join(args))
    logger.info('write summary')
    create_summary(
        project_path=Path(config['DEFAULT']['project']),
        exp_name=Path(config['DEFAULT']['name']),
        dat_path=Path(config['DEFAULT']['source'])
    )

    move_processed_dat(
        Path(config['DEFAULT']['source'])
    )
    shutil.rmtree(
        Path(config['DEFAULT']['source']) / "images"
    )


if __name__ == '__main__':
    try:
        timer_sec = int(config['DEFAULT']['timer_sec'])
        iter_count = int(config['DEFAULT']['iter_count'])
    except ValueError as err:
        sys.exit(str(err))

    s = sched.scheduler()
    for i in range(iter_count):
        s.enter(timer_sec, 0, main)
        s.run()

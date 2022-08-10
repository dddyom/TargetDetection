from configparser import ConfigParser
from loguru import logger
from pathlib import Path
import os
import sys

from utils import mkdir_images_from_dat_path


def get_args() -> list[str]:
    args = []

    config = ConfigParser()
    config.read('config.ini')

    for key in config['DEFAULT']:

        if key == 'source':
            source_dat = Path(config['DEFAULT'][key])
            err = mkdir_images_from_dat_path(source_dat)
            if err:
                sys.exit(err)
            args.append("--{key} {image_path}".format(
                key=key,
                image_path=str(source_dat / 'images'),
            ))
            continue

        if key in ('save-txt', 'save-conf', 'save-crop', 'hide-labels', 'hide-conf'):
            if config['DEFAULT'].getboolean(key):
                args.append('--{key}'.format(
                    key=key,
                ))
            continue

        args.append("--{key} {value}".format(
            key=key,
            value=config['DEFAULT'][key],
        ))
    logger.info('config parsed')
    return args


def main() -> None:
    args = get_args()
    logger.info('start detection')
    os.system('python yolov5/detect.py ' + ' '.join(args))


if __name__ == '__main__':
    main()

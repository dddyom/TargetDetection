from configparser import ConfigParser
import os
import sys

from utils import mkdir_images_from_dat_path


def get_args():
    args = []

    config = ConfigParser()
    config.read('config.ini')

    for key in config['DEFAULT']:

        if key == 'source':
            source_dat = config['DEFAULT'][key]
            err = mkdir_images_from_dat_path(source_dat)
            if err:
                sys.exit(err)
            args.append("--{key} {source_dat}/images".format(
                key=key,
                source_dat=source_dat,
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

    return args


def main():
    args = get_args()
    print(args)
    os.system('python yolov5/detect.py ' + ' '.join(args))


if __name__ == '__main__':
    main()

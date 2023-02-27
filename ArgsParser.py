import sys
from configparser import ConfigParser
from pathlib import Path
from utils import mkdir_images_from_dat_path


class ArgsParser:
    def __init__(self, config_path):
        self.config = ConfigParser()
        self.args = []

        if not self.config.read(config_path):
            sys.exit("Config not found. Uncorrected path to ini file")
        self.format_args_for_predict()

    def format_args_for_predict(self):

        for key in self.config['DEFAULT']:

            if key == 'source':
                self.parse_source_path()

            elif key in ('save-txt', 'save-conf',
                         'save-crop', 'hide-labels', 'hide-conf'):
                self.parse_as_bool_args(key)
            else:
                self.parse_as_value(key)

    def parse_source_path(self):
        source_dat = Path(self.config['DEFAULT']['source'])
        err = mkdir_images_from_dat_path(source_dat)
        if err:
            sys.exit(str(err))
        self.args.append(
            f"--source {str(source_dat / 'images')}"
        )

    def parse_as_bool_args(self, key):
        if self.config['DEFAULT'].getboolean(key):
            self.args.append(f'--{key}')

    def parse_as_value(self, key):
        self.args.append(f"--{key} {self.config['DEFAULT'][key]}")

    def get_args(self):
        return self.args

    def by_key(self, key):
        return self.config['DEFAULT'].get(key)

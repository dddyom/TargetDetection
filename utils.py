from loguru import logger
from pathlib import Path

import os
import re

from Buffer import Buffer
from Labels import Labels


def mkdir_images_from_dat_path(dat_path: Path) -> Exception:
    logger.info('Convert dat to images...')
    try:
        buffers = list(dat_path.iterdir())
    except FileNotFoundError as e:
        return e

    image_path = dat_path / 'images'
    if not os.path.exists(image_path):
        os.mkdir(image_path)

    for buf in sorted(buffers):
        if not re.search("^SO.*dat$", buf.name):
            continue

        jpg_fname = image_path / (buf.stem + '.jpg')
        if jpg_fname.exists():
            continue

        buf_arr = Buffer(dat_file_path=dat_path / buf)
        buf_arr.save_jpg(jpg_fname=jpg_fname)
        logger.info(f"Save {buf.stem}.jpg to {image_path}")


def create_summary(project_path, exp_name):
    summaries = Labels(exp_path=Labels.get_creating_exp_path(
        project_path=project_path,
        exp_name=exp_name
    ))
    summaries.save_txt()
    summaries.save_json()

from pathlib import Path

import os
import re
from loguru import logger

from Buffer import Buffer
from Labels import Labels


def mkdir_images_from_dat_path(dat_path: Path) -> str | None:
    """
    creating directory with jpg files by path with dat files
    """
    logger.info('Convert dat to images...')
    try:
        buffers = list(dat_path.iterdir())
    except FileNotFoundError as err:
        return str(err)

    image_path = dat_path / 'images'
    if not os.path.exists(image_path):
        os.mkdir(image_path)

    for buf in sorted(buffers):
        if not re.search("^SO.*dat$", buf.name):
            continue

        jpg_fname = image_path / (buf.stem + '.jpg')
        if jpg_fname.exists():
            continue

        Buffer(dat_file_path=dat_path / buf).save_jpg(jpg_fname=jpg_fname)
        logger.info(f"Save {buf.stem}.jpg to {image_path}")


def create_summary(project_path, exp_name, dat_path):
    summaries = Labels(exp_path=Labels.get_creating_exp_path(
        project_path=project_path,
        exp_name=exp_name
    ),
        save_path=dat_path)
    summaries.save_txt()
    # summaries.save_json()
    summaries.remove_exp()


def move_processed_dat(dat_path: Path) -> str | None:
    logger.info('Move processed dat...')
    try:
        buffers = list(dat_path.iterdir())
    except FileNotFoundError as err:
        return str(err)

    processed_path = Path.joinpath(dat_path, "processed")
    if not os.path.exists(processed_path):
        os.mkdir(processed_path)

    for buf in sorted(buffers):
        if not re.search("^SO.*dat$", buf.name):
            continue
        Path.rename(buf, processed_path / buf.name)

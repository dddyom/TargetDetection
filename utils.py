import matplotlib.pyplot as plt
from matplotlib.colors import Normalize, LinearSegmentedColormap
from loguru import logger
from pathlib import Path

import numpy as np
import struct
import os
import re


def convert_dat_to_numpy_array(dat_file_path: Path) -> np.ndarray:
    buffer: list[tuple] = []
    dat_file = open(dat_file_path, "rb").read()

    for i in range(0, len(dat_file), 2):
        buffer.append(struct.unpack("<H", dat_file[i: i + 2]))

    matrix = np.reshape(np.array(buffer), (2048, 1200))

    return matrix.T


def get_cmap() -> LinearSegmentedColormap:
    norm = Normalize(-1, 1)
    colors = [[norm(-1.0), "0"],  # black
              [norm(1.0), "yellow"]]

    cmap = LinearSegmentedColormap.from_list("", colors)

    return cmap


def save_numpy_array_to_image(arr: np.ndarray,
                              jpg_fname: Path) -> None:
    cmap = get_cmap()
    plt.imsave(fname=jpg_fname,
               arr=arr,
               cmap=cmap,
               format='jpg')


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

        buf_arr = convert_dat_to_numpy_array(dat_file_path=dat_path / buf)
        logger.info(f"Save {buf.stem}.jpg to {image_path}")
        save_numpy_array_to_image(arr=buf_arr,
                                  jpg_fname=jpg_fname,
                                  )

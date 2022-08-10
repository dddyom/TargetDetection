import matplotlib.pyplot as plt
from matplotlib.colors import Normalize, LinearSegmentedColormap

import numpy as np
import struct
import os
import re


def convert_dat_to_numpy_array(dat_file_path):
    buffer = []
    dat_file = open(dat_file_path, "rb").read()

    for i in range(0, len(dat_file), 2):
        buffer.append(struct.unpack("<H", dat_file[i: i + 2]))

    matrix = np.reshape(np.array(buffer), (2048, 1200))

    return matrix


def get_cmap():
    norm = Normalize(-1, 1)
    colors = [[norm(-1.0), "0"],  # black
              [norm(1.0), "yellow"]]

    cmap = LinearSegmentedColormap.from_list("", colors)

    return cmap


def save_numpy_array_to_image(arr, title, path):
    cmap = get_cmap()
    if not os.path.exists(path):
        os.mkdir(path)
    plt.imsave(fname=f'{path}/{title}.jpg', arr=arr.T, cmap=cmap, format='jpg')


def mkdir_images_from_dat_path(dat_path):
    try:
        buffers = os.listdir(dat_path)
    except FileNotFoundError as e:
        return e
    for buf in sorted(buffers):
        if not re.search("^SO.*dat$", buf):
            continue
        buf_arr = convert_dat_to_numpy_array(dat_file_path=f'{dat_path}/{buf}')
        buf_title = buf.split('.')[0]
        print(f"Save {buf_title}.dat to jpg")
        save_numpy_array_to_image(arr=buf_arr, title=buf_title, path=f'{dat_path}/images')

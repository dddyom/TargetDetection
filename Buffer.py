import struct
from pathlib import Path
import numpy as np
from matplotlib import pyplot as plt
from matplotlib.colors import LinearSegmentedColormap, Normalize

# Colormap creating
norm = Normalize(-1, 1)
CMAP = LinearSegmentedColormap.from_list("",
                                         [[norm(-1.0), "0"],  # black
                                          [norm(1.0), "yellow"]]
                                         )

"""Source buffer cls"""


class Buffer:
    def __init__(self, dat_file_path: Path):
        """Init numpy array from path to SO dat file"""
        buffer = []
        dat_file = open(dat_file_path, "rb").read()

        for i in range(0, len(dat_file), 2):
            buffer.append(struct.unpack("<H", dat_file[i: i + 2]))

        self.matrix = np.reshape(np.array(buffer), (2048, 1200)).T

    def save_jpg(self, jpg_fname: Path) -> None:
        plt.imsave(fname=jpg_fname,
                   arr=self.matrix,
                   cmap=CMAP,
                   format='jpg')

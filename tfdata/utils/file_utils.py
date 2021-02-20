import imghdr
from pathlib import Path
from typing import List

import numpy as np


def obtain_folders(path: Path):
    """Given a path, return the folders present in that path as a list"""
    return [val for val in path.iterdir() if val.is_dir()]


def obtain_files(path: Path):
    """Given a path, return the files present in that path as a list"""
    return [val for val in path.iterdir() if val.is_file()]


def obtain_image_files(path: Path):
    """Given a path, return the image files present in that path as a list"""
    return [val for val in path.iterdir() if (val.is_file() and imghdr.what(val))]


def obtain_image_files_from_folders(folders: List[Path]):
    """Given a path, return the image files present in that path as a list"""
    info = {}
    image_files = []
    for folder in folders:
        temp_image_files = obtain_image_files(folder)
        image_files += temp_image_files
        info["n_image_files"] += [len(temp_image_files)]
    info["cum_n_image_files"] = np.cumsum(info["n_image_files"])
    return image_files, info

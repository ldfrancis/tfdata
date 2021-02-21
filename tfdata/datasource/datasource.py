from collections import defaultdict
from copy import deepcopy
from typing import Callable, Union
from pathlib import Path
import numpy as np
from ..utils.file_utils import obtain_folders, obtain_image_files, obtain_image_files_from_folders


class ImageClassificationDataSource:
    """
    Attributes:
        +image_files
        +n_image_files
        +cum_n_image_files
        +labels
    """

    @classmethod
    def from_folder(cls, folder: Union[str, Path], n_classes: int, class_name_extractor: Callable = None):
        """Creates an image data source from a folder. It is assumed that the folder contains the images which may be
        saved in two different ways;
        1. Images are saved in folders with those belonging to the same class in the same folder. For example, if there
        are 3 classes, the base folder would have 3 folders, each containing images of a certain class.
        2. The folder contains images, each with a name corresponding to the image class.

        Args:
            folder (str or Path): The  base folder containing  images or folders of images
            n_classes (int): The number of classes
            class_name_extractor (function)

        Returns:
            (ImageClassificationDataSource) object

        """
        if isinstance(folder, str):
            folder = Path(folder)
        assert isinstance(folder, Path)

        temp_image_folders = obtain_folders(folder)
        temp_image_files = obtain_image_files(folder)

        # check the contained folders. If the number of folders if equal to the number of classes, then proceed to use
        # the first method to create the data source
        if len(temp_image_folders) == n_classes:
            # images are located in folders
            image_files, info = obtain_image_files_from_folders(temp_image_folders)
            n_image_files = info["n_image_files"]
            cum_n_image_files = info["cum_n_image_files"]
            labels = [val for i, n in enumerate(n_image_files) for val in [i] * n]
        else:  # use second method
            assert class_name_extractor is not None
            files = defaultdict(lambda: [])
            for file in deepcopy(temp_image_files):
                class_name = class_name_extractor(file.name)
                files[class_name] += [file]
                temp_image_files.remove(file)
            image_files = [v for _, values in files.items() for v in values]
            n_image_files = [len(v) for _, v in files.items()]
            cum_n_image_files = np.cumsum(n_image_files)
            labels = [val for i, n in enumerate(n_image_files) for val in [i] * n]

        ds = cls()
        ds.image_files = image_files
        ds.n_image_files = n_image_files
        ds.cum_n_images = cum_n_image_files
        ds.labels = labels
        return ds

    def __init__(self):
        pass

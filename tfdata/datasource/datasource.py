from abc import ABC, abstractmethod, abstractproperty
from collections import defaultdict
from copy import deepcopy

from ..dataloader import DataLoader
from pathlib import Path
import logging
import imghdr
import numpy as np


class DataSource(ABC):

    def __init__(self, source):
        self.source = source

    def make_loader(self):
        return DataLoader(self)


class ImageDataSource(DataSource):

    @staticmethod
    def from_folder(folder, n_classes, class_name_extractor=None):
        """Creates an image data source from a folder. It is assumed that the folder contains the images which may be
        saved in two different ways;
        1. Images are saved in folders with those belonging to the same class in the same folder. For example, if there
        are 3 classes, the base folder would have 3 folders, each containing images of a certain class.
        2. The folder contains images, each with a name corresponding to the image class.
        """
        if isinstance(folder, str):
            folder = Path(folder)

        assert isinstance(folder, Path)

        # check the contained folders. If the number of folders if equal to the number of classes, then proceed to use
        # the first method to create the data source
        temp_image_folders = []
        temp_folder_names = []
        temp_image_files = []
        temp_image_filenames = []
        for dir_or_file in folder.iterdir():
            if dir_or_file.is_dir():
                temp_image_folders += [dir_or_file]
                temp_folder_names += [dir_or_file.name]
            if dir_or_file.is_file() and imghdr.what(dir_or_file):
                temp_image_files += [dir_or_file]
                temp_image_filenames += [dir_or_file.name]
            if len(temp_image_folders) > n_classes:
                temp_image_folders = []
                logging.info("Folder does not have class images contained in folders")

        # check whether to use first method of data source creation or not
        if temp_image_folders:
            # images are located in folders
            images = []
            n_images = []
            labels = []
            name_of_folders = temp_folder_names
            for i, folder in enumerate(temp_image_folders):
                folder_images = [file for file in folder.iterdir() if (file.is_file() and imghdr.what(file))]
                images += folder_images
                n_images += [len(folder_images)]
                labels += [i]*len(folder_images)
            n_indices = np.prod(n_images)
            cum_n_images = np.cumsum(n_images)

        else:  # use second method
            assert class_name_extractor is not None
            files = defaultdict(lambda : [])
            for file in deepcopy(temp_image_files):
                class_name = class_name_extractor(file.name)
                files[class_name] += [file]
                temp_image_files.remove(file)
            images = [v for _, values in files.items() for v in values]
            n_images = [len(v) for _, v in files.items()]
            n_indices = np.prod(n_images)
            cum_n_images = np.cumsum(n_images)








    def __init__(self):
        super().__init__()

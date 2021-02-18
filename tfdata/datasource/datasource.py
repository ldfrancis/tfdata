from abc import ABC, abstractmethod, abstractproperty
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
    def from_folder(folder, n_classes, ):
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
        for dir_or_file in folder.iterdir():
            if dir_or_file.is_dir():
                temp_image_folders += [dir_or_file]
                temp_folder_names += [dir_or_file.name]
            if len(temp_image_folders) > n_classes:
                temp_image_folders = []
                logging.info("Folder does not have class images contained in folders")

        # check whether to use first method of data source creation or not
        if temp_image_folders:
            # images are located in folders
            images_in_folders = []
            n_images_in_folders = []
            name_of_folders = temp_folder_names
            for folder in temp_image_folders:
                images = [file for file in folder.iterdir() if (file.is_file() and imghdr.what(file))]
                images_in_folders += [images]
                n_images_in_folders += [len(images)]
            n_indices = np.prod(n_images_in_folders)

    def __init__(self):
        super().__init__()

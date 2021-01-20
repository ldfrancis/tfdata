from .datasource import DataSource
from pathlib import Path
import imghdr

class ImageDataSource(DataSource):

    def __init__(self, source):
        super().__init__(source)
        self.source = Path(source)
        self.files = [file for file in self.source.iterdir() \
                        if (file.is_file() and imghdr.what(file))]

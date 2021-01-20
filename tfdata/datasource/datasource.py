from abc import ABC, abstractmethod, abstractproperty
from ..dataloader import DataLoader

class DataSource(ABC):

    def __init__(self, source):
        self.source = source

    def make_loader(self):
        return DataLoader(self)
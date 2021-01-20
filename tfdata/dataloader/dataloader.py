
class DataLoader:

    def __init__(self, datasource):
        self.datasource = datasource
        self.indx = 0

    def __iter__(self):
        return self

    def __next__(self):
        if self.indx >= len(self):
            raise StopIteration
        ind = self.indx
        self.indx +=1
        return self.datasource.files[ind]

    def __getitem__(self, idx):
        return self.datasource.files[idx]

    def __len__(self):
        return len(self.datasource.files)

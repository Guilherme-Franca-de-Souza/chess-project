from torch.utils.data import Dataset
import h5py
import torch
import torch.nn as nn # type: ignore
import torch.optim as optim # type: ignore
from torch.utils.data import DataLoader # type: ignore

class ChessHDF5Dataset(Dataset):
    def __init__(self, hdf5_file_path):
        self.h5_file = h5py.File(hdf5_file_path, 'r')
        self.X = self.h5_file['X']
        self.y = self.h5_file['y']
        self.length = self.X.shape[0]
        
    def __len__(self):
        return self.length
    
    def __getitem__(self, idx):
        X = torch.tensor(self.X[idx], dtype=torch.float32)
        y = torch.tensor(self.y[idx], dtype=torch.float32)
        return X, y

    def close(self):
        self.h5_file.close()
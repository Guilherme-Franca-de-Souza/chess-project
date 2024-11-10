#IMPORTS
import os
import numpy as np # type: ignore
import time
import torch
import torch.nn as nn # type: ignore
import torch.optim as optim # type: ignore
from torch.utils.data import DataLoader # type: ignore
from chess import pgn # type: ignore
from tqdm import tqdm # type: ignore

#DATA PROCESSING

## Convert data into tensors
from auxiliary_func import create_input_for_nn

import pandas as pd

import h5py
import torch

#pega o array de avaliações e transforma em tensors
# X transforma naquela matriz, e y os resultados
# tem 120 milhões de avaliações
# pega apenas 24 partes de 100 mil
# ou seja 2.400.000, dois milhões e 400 mil


## PRIMEIRO TRANSFORMA AS AVALIAÇÕES EM TENSORES
# X = REPRESENTAÇÃO DO TABULEIRO EM MATRIZ
# Z = AVALIACOES (LABELS) DO STOCKFISH
'''
csv_file = '../avaliacoes.csv'

for i in range(0, 24):
    skip = ((i * 100000)+2)
    avaliacoes = pd.read_csv(csv_file, skiprows=skip, nrows=100000)

    X, y = create_input_for_nn(avaliacoes)

    X = X[0:100000]
    y = y[0:100000]

    X = torch.tensor(X, dtype=torch.float32)
    y = torch.tensor(y, dtype=torch.float32)

    torch.save(X, f'X_tensor_{i}.pt')
    torch.save(y, f'y_tensor_{i}.pt')
'''

## DEPOIS
## Concatena os tensors e salva como hdf5
## altera o dataset para lidar com esse tipo de arquivo
'''
# Crie o arquivo HDF5
with h5py.File('chess_data.h5', 'w') as h5f:
    # Determine o tamanho total dos seus dados
    total_size = 0
    for i in range(0, 24):
        X_part = torch.load(f'X_tensor_{i}.pt')
        total_size += len(X_part)

    # Obtenha as dimensões dos dados
    X_shape = X_part.shape[1:]
    y_shape = (1,)  # y é um valor escalar para cada amostra

    # Crie datasets HDF5 com as dimensões totais
    X_h5 = h5f.create_dataset('X', shape=(total_size, *X_shape), dtype='float32')
    y_h5 = h5f.create_dataset('y', shape=(total_size, *y_shape), dtype='float32')

    # Preencha o arquivo HDF5 com os dados em partes
    start_idx = 0
    for i in range(0, 24):
        X_part = torch.load(f'X_tensor_{i}.pt')
        y_part = torch.load(f'y_tensor_{i}.pt')
        end_idx = start_idx + len(X_part)

        X_h5[start_idx:end_idx] = X_part.numpy()
        y_h5[start_idx:end_idx] = y_part.numpy().reshape(-1, 1)

        start_idx = end_idx
'''
# realiza o treinamento e salva
from torch.utils.data import DataLoader

from dataset import ChessHDF5Dataset
from model import ChessModel

# Crie uma instância do dataset
dataset = ChessHDF5Dataset('chess_data.h5')
dataloader = DataLoader(dataset, batch_size=64, shuffle=True)

print(torch.cuda.is_available())
# Treinamento
device = torch.device("cuda" if torch.cuda.is_available() else "cpu")
print(torch.cuda.is_available())

model = ChessModel().to(device)  # Certifique-se de que seu modelo esteja inicializado corretamente
criterion = nn.MSELoss()
optimizer = optim.Adam(model.parameters(), lr=0.0001)

num_epochs = 50
for epoch in range(num_epochs):
    start_time = time.time()
    model.train()
    running_loss = 0.0
    for inputs, labels in tqdm(dataloader):
        inputs, labels = inputs.to(device), labels.to(device)
        
        optimizer.zero_grad()
        outputs = model(inputs)
        
        loss = criterion(outputs, labels)
        loss.backward()
        
        torch.nn.utils.clip_grad_norm_(model.parameters(), max_norm=1.0)
        
        optimizer.step()
        running_loss += loss.item()
    end_time = time.time()
    epoch_time = end_time - start_time
    minutes: int = int(epoch_time // 60)
    seconds: int = int(epoch_time) - minutes * 60
    print(f'Epoch {epoch + 1}/{num_epochs}, Loss: {running_loss / len(dataloader):.4f}')

torch.save(model.state_dict(), "../../models/TORCH17_50EPOCHS.pth")

# Feche o dataset HDF5 ao final do treinamento
dataset.close()



'''
# Preliminary actions

from dataset import ChessDataset
from model import ChessModel

# Create Dataset and DataLoader
dataset = ChessDataset(X, y)
dataloader = DataLoader(dataset, batch_size=64, shuffle=True)

# Check for GPU
device = torch.device("cuda" if torch.cuda.is_available() else "cpu")
print(f'Using device: {device}')

# Model Initialization
model = ChessModel(num_classes=num_classes).to(device)
criterion = nn.CrossEntropyLoss()
optimizer = optim.Adam(model.parameters(), lr=0.0001)

# TRAINING

num_epochs = 50
for epoch in range(num_epochs):
    start_time = time.time()
    model.train()
    running_loss = 0.0
    for inputs, labels in tqdm(dataloader):
        inputs, labels = inputs.to(device), labels.to(device)  # Move data to GPU
        optimizer.zero_grad()

        outputs = model(inputs)  # Raw logits

        # Compute loss
        loss = criterion(outputs, labels)
        loss.backward()
        
        # Gradient clipping
        torch.nn.utils.clip_grad_norm_(model.parameters(), max_norm=1.0)
        
        optimizer.step()
        running_loss += loss.item()
    end_time = time.time()
    epoch_time = end_time - start_time
    minutes: int = int(epoch_time // 60)
    seconds: int = int(epoch_time) - minutes * 60
    print(f'Epoch {epoch + 1 + 50}/{num_epochs + 1 + 50}, Loss: {running_loss / len(dataloader):.4f}, Time: {minutes}m{seconds}s')

# Save the model
torch.save(model.state_dict(), "../../models/TORCH_100EPOCHS.pth")
'''
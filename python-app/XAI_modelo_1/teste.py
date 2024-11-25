import chess
import chess.engine
import torch
from auxiliary_func import board_to_matrix
from model import ChessModel
from explainability import smoothgrad, lime_explain, deeplift, saliency_map, gradcam, lrp
import matplotlib.pyplot as plt
import numpy as np

model = ChessModel()
input_tensor = torch.rand(1, 13, 8, 8)  # Formato especificado

print("Running LRP with Debugging...")
try:
    relevance = lrp(model, input_tensor)
    print("Relevance Computed Successfully:", relevance.shape)
except Exception as e:
    print("An error occurred during LRP execution:")
    print(e)

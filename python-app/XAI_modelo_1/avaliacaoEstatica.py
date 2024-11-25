import chess
import chess.engine
import torch
from auxiliary_func import board_to_matrix
from model import ChessModel
from explainability import smoothgrad, lime_explain, deeplift, saliency_map, gradcam, lrp
import matplotlib.pyplot as plt
import numpy as np

class StaticEvaluatorRN:
    def __init__(self):
        device = torch.device("cuda" if torch.cuda.is_available() else "cpu")
        self.device = device
        model = ChessModel().to(device)
        model.load_state_dict(torch.load("evaluator.pth", map_location=device, weights_only=False))
        model.eval()
        self.model = model

    def prepare_input(self, board: chess.Board):
        matrix = board_to_matrix(board)
        X_tensor = torch.tensor(matrix, dtype=torch.float32).unsqueeze(0)
        return X_tensor.to(self.device)

    def evaluate(self, board: chess.Board):
        X_input = self.prepare_input(board)
        with torch.no_grad():
            prediction = self.model(X_input)
        return prediction.item()

evaluator = StaticEvaluatorRN()

def analyze_position_with_model(fen):
    board = chess.Board(fen)
    print(evaluator.evaluate(board))


# Exemplo de uso
fen = "rbnqk1nr/1ppppbpp/8/1BN3B1/pN2P3/3R1Q2/1P3KPP/3R4 b kq - 0 1"
analyze_position_with_model(fen)
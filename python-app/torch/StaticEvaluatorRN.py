import torch
import chess
import chess.engine
from chess import Board, pgn
from model import ChessModel
from auxiliary_func import board_to_matrix
import StockfishEngineEval

class StaticEvaluatorRN:
    def __init__(self):
        device = torch.device("cuda" if torch.cuda.is_available() else "cpu")
        self.device = device
        model = ChessModel().to(device)
        model.load_state_dict(torch.load("evaluator.pth", map_location=device, weights_only=True))
        model.eval()
        self.model = model

    def prepare_input(self, board: Board):
        matrix = board_to_matrix(board)
        X_tensor = torch.tensor(matrix, dtype=torch.float32).unsqueeze(0)
        return X_tensor

    def evaluate(self, board: Board):
        X_input = self.prepare_input(board)

        X_input_tensor = X_input.to(self.device)

        with torch.no_grad():
            prediction = self.model(X_input_tensor)

        predicted_score = prediction.item()

        return predicted_score

evaluator = StaticEvaluatorRN()

# Função de avaliação que usa a instância global
def evaluate(board):
    return evaluator.evaluate(board)
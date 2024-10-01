import torch
import chess
import chess.engine
from chess import Board, pgn
from model import ChessModel
from auxiliary_func import board_to_matrix
import StockfishEngineEval

def prepare_input(board: Board):
    matrix = board_to_matrix(board)
    X_tensor = torch.tensor(matrix, dtype=torch.float32).unsqueeze(0)
    return X_tensor

device = torch.device("cuda" if torch.cuda.is_available() else "cpu")
model = ChessModel().to(device)
model.load_state_dict(torch.load("TORCH_100EPOCHS.pth", map_location=device, weights_only=True))
model.eval()

fen = "rnbqk1nr/1ppppbp1/8/1B2P1B1/p2PN2p/2N5/1PP2PPP/R2QK2R w KQ - 0 1"
board = chess.Board(fen)

X_input = prepare_input(board)

X_input_tensor = X_input.to(device)

with torch.no_grad():
    prediction = model(X_input_tensor)

predicted_score = prediction.item()

stockfish_score = StockfishEngineEval.eval(fen)
print(f"IA: {predicted_score}")
print(f"Stockfish: {stockfish_score}")
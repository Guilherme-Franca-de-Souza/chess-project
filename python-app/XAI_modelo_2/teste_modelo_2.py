from chess import Board, pgn
from auxiliary_func import board_to_matrix
import torch
from model import ChessModel
import pickle
import numpy as np
import chess.engine

def prepare_input(board: Board):
    matrix = board_to_matrix(board)
    X_tensor = torch.tensor(matrix, dtype=torch.float32).unsqueeze(0)
    return X_tensor

# Load the mapping
with open("move_to_int", "rb") as file:
    move_to_int = pickle.load(file)

# Check for GPU
device = torch.device("cuda" if torch.cuda.is_available() else "cpu")
print(f'Using device: {device}')

# Load the model
model = ChessModel(num_classes=len(move_to_int))
model.load_state_dict(torch.load("player.pth", map_location=device))
model.to(device)
model.eval()  # Set the model to evaluation mode

int_to_move = {v: k for k, v in move_to_int.items()}

# Function to make predictions
def predict_move(board: Board):
    X_tensor = prepare_input(board).to(device)
    
    with torch.no_grad():
        logits = model(X_tensor)
    
    logits = logits.squeeze(0)  # Remove batch dimension
    probabilities = torch.softmax(logits, dim=0).cpu().numpy()  # Convert to probabilities
    legal_moves = list(board.legal_moves)
    legal_moves_uci = [move.uci() for move in legal_moves]
    sorted_indices = np.argsort(probabilities)[::-1]
    
    for move_index in sorted_indices:
        move = int_to_move[move_index]
        if move in legal_moves_uci:
            return move
    
    return None

# Initialize a chess board
board = Board()

# Initialize Stockfish engine
with chess.engine.SimpleEngine.popen_uci("/usr/games/stockfish") as engine:
    while not board.is_game_over():
        # Your model plays as white
        best_move = predict_move(board)
        board.push_uci(best_move)
        print(f'Your move: {best_move}')
        print(board)

        # Check if the game is over after white's move
        if board.is_game_over():
            break

        # Stockfish plays as black
        result = engine.play(board, chess.engine.Limit(depth=1))  # Adjust time as necessary
        board.push(result.move)
        print(f'Stockfish move: {result.move}')
        print(board)

    print("Game over!")
    print(str(pgn.Game.from_board(board)))
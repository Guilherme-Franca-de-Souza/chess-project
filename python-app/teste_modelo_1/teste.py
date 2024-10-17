import pandas as pd
import chess
import torch
from auxiliary_func import board_to_matrix
from model import ChessModel

def load_positions(csv_file, n_positions=10000, skip_rows=3000000):
    column_names = ['fen', 'evaluation']
    df = pd.read_csv(csv_file, skiprows=skip_rows, nrows=n_positions, header=None, names=column_names)
    df['evaluation'] = df['evaluation'].astype(float)
    return df

def prepare_input(board, device):
    matrix = board_to_matrix(board)
    X_tensor = torch.tensor(matrix, dtype=torch.float32).unsqueeze(0)
    return X_tensor.to(device)

def evaluate_model(model, board, device):
    X_input = prepare_input(board, device)
    with torch.no_grad():
        prediction = model(X_input)
    return prediction.item()

def analyze_evaluations(csv_file, model, device, output_csv):
    df = load_positions(csv_file)
    results = []

    for index, row in df.iterrows():
        fen = row['fen']
        stockfish_evaluation = row['evaluation']
        
        board = chess.Board(fen)
        model_prediction = evaluate_model(model, board, device)

        results.append({
            'fen': fen,
            'stockfish_evaluation': stockfish_evaluation,
            'model_prediction': model_prediction,
            'error': model_prediction - stockfish_evaluation
        })

    results_df = pd.DataFrame(results)
    
    results_df.to_csv(output_csv, index=False)

if __name__ == "__main__":
    csv_file = 'avaliacoes-01.csv'
    output_csv = 'resultados_avaliacoes.csv'
    device = torch.device('cuda' if torch.cuda.is_available() else 'cpu')

    model = ChessModel().to(device)
    model.load_state_dict(torch.load("evaluator.pth", map_location=device, weights_only=False))  # Caminho do seu modelo
    model.eval()

    analyze_evaluations(csv_file, model, device, output_csv)
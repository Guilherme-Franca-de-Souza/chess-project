import chess
import chess.engine
import torch
from auxiliary_func import board_to_matrix
from model import ChessModel
from explainability import smoothgrad, lime_explain, shap_explain, gradcam, lrp
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

    def explain(self, board: chess.Board, method: str):
        X_input = self.prepare_input(board)
        if method == "smoothgrad":
            return smoothgrad(self.model, X_input)
        elif method == "lime":
            return lime_explain(self.model, X_input, board_to_matrix)
        elif method == "shap":
            return shap_explain(self.model, X_input)
        elif method == "gradcam":
            return gradcam(self.model, X_input)
        elif method == "lrp":
            return lrp(self.model, X_input)
        else:
            raise ValueError("Método de explicabilidade não reconhecido.")


def save_explanation(explanation, method, move_num):
    output_path_template = f"{method}/explanation_move_{move_num}_channel_{{}}.png"

    if method == "lime":
        # Pegar as contribuições das features (importância das features explicadas)
        feature_importances = explanation.as_list()  # Lista de pares (feature, weight)
        
        # Separar features e pesos
        features, weights = zip(*feature_importances)
        
        # Plotar a importância das features
        plt.figure(figsize=(10, 6))
        plt.barh(features, weights)
        plt.xlabel("Peso")
        plt.ylabel("Features")
        plt.title(f"Importância das Features - Jogada {move_num}")
        plt.savefig(f"explanation_{method}_move_{move_num}.png")
        plt.close()
    
    elif method == "shap":
        # Supondo que "explanation" tenha a forma (1, 13, 8, 8, 1)
        explanation_slices = explanation[0, :, :, :, 0]  # Remover dimensões extras
        
        # Criar subplots para visualizar várias fatias
        fig, axes = plt.subplots(4, 4, figsize=(10, 10))
        
        for i in range(13):
            ax = axes[i // 4, i % 4]
            ax.imshow(explanation_slices[i], cmap='viridis', interpolation='none')
            ax.set_title(f'Feature {i}')
        
        plt.suptitle(f"Importância das Features - Jogada {move_num}")
        plt.tight_layout()
        plt.savefig(f"explanation_{method}_move_{move_num}.png")
        plt.close()


    # Se a explicação for uma matriz 4D, dividir os canais em imagens separadas
    elif isinstance(explanation, np.ndarray) and explanation.ndim == 4:  # (1, 13, 8, 8)
        explanation = explanation.squeeze()  # Remove a dimensão de batch (fica (13, 8, 8))

        # Criar uma imagem para cada canal
        for i in range(explanation.shape[0]):  # Explicação agora tem (13, 8, 8)
            plt.imshow(explanation[i], cmap='hot', interpolation='nearest')
            plt.colorbar()

            output_path = output_path_template.format(i + 1)  # Para numerar os canais
            plt.savefig(output_path)
            plt.close()

            print(f"Explicação canal {i+1} salva em {output_path}")
    else:
        # Outros tipos de explicações (como gráficos de importâncias de características)
        plt.plot(explanation)
        plt.title(f"Explicação {method} - Jogada {move_num}")
        plt.xlabel("Características")
        plt.ylabel("Importância")

        output_path = f"explanation_{method}_move_{move_num}.png"
        plt.savefig(output_path)
        plt.close()
        print(f"Explicação salva em {output_path}")

evaluator = StaticEvaluatorRN()

# Inicializa o Stockfish (substitua o caminho pelo local onde o stockfish está instalado)
engine = chess.engine.SimpleEngine.popen_uci("/usr/games/stockfish")

def get_best_lines(fen, depth=20):
    board = chess.Board(fen)
    result = engine.analyse(board, chess.engine.Limit(depth=depth), multipv=2)

    best_lines = []
    for info in result:
        line_moves = info["pv"]  # "pv" contém a sequência de jogadas (principal variation)
        best_lines.append(line_moves)

    return best_lines

def analyze_position_with_model(fen, depth=2, method="smoothgrad"):
    best_lines = get_best_lines(fen, depth)
    board = chess.Board(fen)

    for i, line in enumerate(best_lines):
        print(f"\nLinha {i+1}:")
        print(f"Avaliação da posição inicial: {evaluator.evaluate(board)}")

        for move_num, move in enumerate(line):
            board.push(move)
            static_evaluation = evaluator.evaluate(board)
            print(f"Jogada {move}: Avaliação {static_evaluation}")

            explanation = evaluator.explain(board, method)
            save_explanation(explanation, method, move_num + 1)

        # Volta o tabuleiro para a posição inicial após cada linha de jogadas
        board = chess.Board(fen)

# Exemplo de uso
fen = "rnbqkbnr/pppppppp/8/8/8/8/PPPPPPPP/RNBQKBNR w KQkq - 0 1"
analyze_position_with_model(fen, depth=20, method="shap")

engine.quit()

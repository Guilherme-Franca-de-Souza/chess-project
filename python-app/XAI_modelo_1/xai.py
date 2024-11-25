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

    def explain(self, board: chess.Board, method: str):
        X_input = self.prepare_input(board)
        if method == "smoothgrad":
            return smoothgrad(self.model, X_input)
        elif method == "lime":
            return lime_explain(self.model, X_input, board_to_matrix)
        elif method == "gradcam":
            return gradcam(self.model, X_input)
        elif method == "lrp":
            return lrp(self.model, X_input)
        elif method == "deeplift":
            return deeplift(self.model, X_input)
        elif method == "saliency_map":
            return saliency_map(self.model, X_input)
        else:
            raise ValueError("Método de explicabilidade não reconhecido.")


def save_explanation(explanation, method, move_num):
    output_path_template = f"{method}/explanation_move_{move_num}_channel_{{}}.png"

    if method == "lime":
        # Pegar as contribuições das features (importância das features explicadas)
        feature_importances = explanation.as_list()  # Lista de pares (feature, weight)
        
        # Separar features e pesos
        features, weights = zip(*feature_importances)
        # Garantir que as features têm nomes descritivos
        features = [f"{feature}" for feature in features]
        # Plotar a importância das features
        plt.figure(figsize=(20, 12))
        plt.barh(features, weights)
        plt.xlabel("Peso")
        plt.ylabel("Features (Canal e Posição)")
        plt.title(f"Importância das Features - Jogada {move_num}")
        plt.savefig(f"{method}/explanation_move_{move_num}.png")
        plt.close()
    
    # Se a explicação for uma matriz 4D, dividir os canais em imagens separadas
    elif isinstance(explanation, np.ndarray) and explanation.ndim == 4:  # (1, 13, 8, 8)
        explanation = explanation.squeeze()  # Remove a dimensão de batch (fica (13, 8, 8))

        # Soma dos primeiros 12 canais
        summed_matrix = np.sum(explanation[:12], axis=0)  # Soma ao longo dos 12 primeiros canais
        plt.imshow(np.flip(summed_matrix, axis=0), cmap='hot', interpolation='nearest')
        plt.colorbar()
        plt.title("Soma das Relevâncias nos 12 Primeiros Canais")
        summed_output_path = f"{method}/absu_summed_explanation_move_{move_num}.png"
        plt.savefig(summed_output_path)
        plt.close()
        print(f"Soma dos primeiros 12 canais salva em {summed_output_path}")

        # Plotar separadamente o 13º canal (jogadas legais)
        channel_13 = explanation[12]  # Obtém o 13º canal (dimensão 12)
        plt.imshow(np.flip(channel_13, axis=0), cmap='hot', interpolation='nearest')
        plt.colorbar()
        plt.title("Relevância do 13º Canal (Jogadas Legais)")
        channel_13_output_path = f"{method}/absu_explanation_move_{move_num}_separated_channel_13.png"
        plt.savefig(channel_13_output_path)
        plt.close()
        print(f"13º canal salvo em {channel_13_output_path}")

        # Criar uma imagem para cada canal
        for i in range(explanation.shape[0]):  # Explicação agora tem (13, 8, 8)
            # Inverter o eixo horizontal ou vertical para ajustar à visualização do tabuleiro
            explanation_channel = np.flip(explanation[i], axis=0)  # Inverter verticalmente (y)
            plt.imshow(explanation_channel, cmap='hot', interpolation='nearest')
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
engine = chess.engine.SimpleEngine.popen_uci("/usr/local/bin/sf17/stockfish")

def analyze_position_with_model(fen):
    board = chess.Board(fen)

    linha_de_lances = [
        chess.Move.from_uci('e3e4'),
    ]

    for i, lance in enumerate(linha_de_lances):
        #print(f"Avaliação da posição inicial: {evaluator.evaluate(board)}")
        board.push(lance)
        static_evaluation = evaluator.evaluate(board)
        #print(f"Jogada {move}: Avaliação {static_evaluation}")
        #explanation = evaluator.explain(board, "smoothgrad")
        #save_explanation(explanation, "smoothgrad", i + 1)
        #explanation = evaluator.explain(board, "lime")
        #save_explanation(explanation, "lime", i + 1)
        explanation = evaluator.explain(board, "lrp")
        save_explanation(explanation, "lrp", i + 1)
        #explanation = evaluator.explain(board, "deeplift")
        #save_explanation(explanation, "deeplift", i + 1)
        #explanation = evaluator.explain(board, "saliency_map")
        #save_explanation(explanation, "saliency_map", i + 1)
        

# Exemplo de uso
fen = "rbnqk1nr/1ppppbpp/8/1BN3B1/pN6/3RPQ2/1P3KPP/3R4 w kq - 0 1"
analyze_position_with_model(fen)

engine.quit()
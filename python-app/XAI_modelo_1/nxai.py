import chess
import chess.engine
import torch
from auxiliary_func import board_to_matrix
from model import ChessModel
from explainability import smoothgrad, lime_explain, deeplift, saliency_map, gradcam, lrp
import matplotlib.pyplot as plt
import numpy as np
from eval import eval

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


def save_explanation(explanation, method, cemario):
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
        plt.title(f"Importância das Features - Jogada {cemario}")
        plt.savefig(f"{method}/explanation_move_{cemario}.png")
        plt.close()
    
    # Se a explicação for uma matriz 4D, dividir os canais em imagens separadas
    elif isinstance(explanation, np.ndarray) and explanation.ndim == 4:  # (1, 13, 8, 8)
        explanation = explanation.squeeze()  # Remove a dimensão de batch (fica (13, 8, 8))

        # Soma dos primeiros 12 canais
        summed_matrix = np.sum(explanation[:12], axis=0)  # Soma ao longo dos 12 primeiros canais
        plt.imshow(np.flip(summed_matrix, axis=0), cmap='hot', interpolation='nearest')
        plt.colorbar()
        plt.title("Soma das Relevâncias nos 12 Primeiros Canais")

        # Adicionando valores dentro dos quadrados
        for i in range(summed_matrix.shape[0]):
            for j in range(summed_matrix.shape[1]):
                if abs(summed_matrix[i, j]) > 1000:
                    value = f"{summed_matrix[i, j]:.2e}"  # Notação científica
                else:
                    value = f"{summed_matrix[i, j]:.2f}"  # Formato com 2 casas decimais
                plt.text(j, summed_matrix.shape[0] - 1 - i, f"{value}", 
                         ha="center", va="center", color="green", fontsize=6)

        summed_output_path = f"{method}/summed_channel_12_explanation_{cemario}.png"
        plt.savefig(summed_output_path)
        plt.close()
        print(f"Soma dos primeiros 12 canais salva em {summed_output_path}")

        # Plotar separadamente o 13º canal (jogadas legais)
        channel_13 = explanation[12]  # Obtém o 13º canal (dimensão 12)
        plt.imshow(np.flip(channel_13, axis=0), cmap='hot', interpolation='nearest')
        plt.colorbar()
        plt.title("Relevância do 13º Canal (Jogadas Legais)")

        # Adicionando valores dentro dos quadrados
        for i in range(channel_13.shape[0]):
            for j in range(channel_13.shape[1]):
                if abs(channel_13[i, j]) > 1000:
                    value = f"{channel_13[i, j]:.2e}"  # Notação científica
                else:
                    value = f"{channel_13[i, j]:.2f}"  # Formato com 2 casas decimais
                plt.text(j, channel_13.shape[0] - 1 - i, f"{value}", 
                         ha="center", va="center", color="green", fontsize=6)

        channel_13_output_path = f"{method}/separated_channel_13_explanation_{cemario}.png"
        plt.savefig(channel_13_output_path)
        plt.close()
        print(f"13º canal salvo em {channel_13_output_path}")

        '''
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
        '''
    else:
        # Outros tipos de explicações (como gráficos de importâncias de características)
        plt.plot(explanation)
        plt.title(f"Explicação {method} - Jogada {cenario}")
        plt.xlabel("Características")
        plt.ylabel("Importância")

        output_path = f"explanation_{method}_move_{cenario}.png"
        plt.savefig(output_path)
        plt.close()
        print(f"Explicação salva em {output_path}")

evaluator = StaticEvaluatorRN()

# Inicializa o Stockfish (substitua o caminho pelo local onde o stockfish está instalado)
engine = chess.engine.SimpleEngine.popen_uci("/usr/local/bin/sf17/stockfish")

def analyze_position_with_model(fen, cenario):
    board = chess.Board(fen)
    #print(f"Jogada {move}: Avaliação {static_evaluation}")
    #explanation = evaluator.explain(board, "smoothgrad")
    #save_explanation(explanation, "smoothgrad", i + 1)
    #explanation = evaluator.explain(board, "lime")
    #save_explanation(explanation, "lime", i + 1)
    explanation = evaluator.explain(board, "lrp")
    save_explanation(explanation, "lrp", cenario)
    explanation = evaluator.explain(board, "deeplift")
    save_explanation(explanation, "deeplift", cenario)
    #explanation = evaluator.explain(board, "saliency_map")
    #save_explanation(explanation, "saliency_map", i + 1)
        

# Exemplo de uso
cenario = 'vp'
fen = "r1bqk1nr/pp1p1ppp/1bnP4/1p2P3/8/5N2/PP3PPP/RNBQ1RK1 b kq - 0 1"
analyze_position_with_model(fen, cenario)
cenario = 'vpa'
fen = "rbnqk1nr/1ppppbpp/8/1BN3B1/pN2P3/3R1Q2/1P3KPP/3R4 b kq - 0 1"
analyze_position_with_model(fen, cenario)
cenario = 'cc'
fen = "rnbqkbnr/2pppp2/1p4p1/p6p/3PP3/2P2P2/PP4PP/RNBQKBNR w KQkq - 0 1"
analyze_position_with_model(fen, cenario)
cenario = 'pp'
fen = "5rk1/4pppp/8/4P3/5P2/6P1/P1P4P/5RK1 w - - 0 1"
analyze_position_with_model(fen, cenario)
cenario = 'ppc'
fen = "5rk1/4pppp/8/4P3/5P2/6P1/PP5P/5RK1 w - - 0 1"
analyze_position_with_model(fen, cenario)

engine.quit()
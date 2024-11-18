'''
# Aparentemente o stockfish guarda em cache avaliações de uma posição
# então se eu chamar essa função várias vezes para a mesma posição
# Ele vai sempre melhorar a análise
def get_best_lines(engine, board, depth=20, multipv=1):
    info = engine.analyse(board, chess.engine.Limit(depth=depth), multipv=multipv)
    return info

# Mostra as linhas de uma forma menos poluida
def get_line_str(line):
    line_str = ', '.join([move.uci() for move in line])
    return line_str
'''

import chess
import chess.engine
import time
import os  # Para limpar o terminal

def get_best_lines_live(engine, board, depth=20, multipv=2, update_interval=1):
    """
    Exibe continuamente as melhores linhas do Stockfish no terminal.
    
    :param engine: Instância da engine do Stockfish.
    :param board: Objeto chess.Board representando a posição atual.
    :param depth: Profundidade de análise da engine.
    :param multipv: Número de melhores linhas a exibir (default: 2).
    :param update_interval: Intervalo entre atualizações no terminal (em segundos).
    """
    try:
        while True:
            # Obtenha as análises da engine
            result = engine.analyse(board, chess.engine.Limit(depth=depth), multipv=multipv)
            
            # Limpe o terminal para uma exibição "ao vivo"
            os.system('cls' if os.name == 'nt' else 'clear')
            
            print("Analisando posição ao vivo...\n")
            for i, info in enumerate(result, start=1):
                line = info["pv"]  # Obter a principal variação (lista de movimentos)
                evaluation = info["score"].relative.score(mate_score=10000)  # Avaliação
                eval_str = f"Mate em {info['score'].relative.mate()}" if info["score"].relative.is_mate() else f"{evaluation / 100:.2f}"
                line_str = get_line_str(line)
                
                print(f"Linha {i}:")
                print(f"  Avaliação: {eval_str}")
                print(f"  Jogadas: {line_str}\n")
            
            # Esperar antes de atualizar novamente
            time.sleep(update_interval)
    except KeyboardInterrupt:
        print("\nAnálise interrompida pelo usuário.")

def get_line_str(line):
    """
    Formata uma linha de jogadas para exibição.
    
    :param line: Lista de movimentos da engine.
    :return: String formatada das jogadas.
    """
    return ', '.join([move.uci() for move in line])

# Exemplo de uso
if __name__ == "__main__":
    # Inicializa o tabuleiro e a engine
    fen = 'r1bqk1nr/pp1pnppp/1bp5/1B6/3PP3/5N2/PP3PPP/RNBQ1RK1 w kq - 0 1'
    board = chess.Board(fen)
    with chess.engine.SimpleEngine.popen_uci("/usr/local/bin/sf17/stockfish") as engine:
        get_best_lines_live(engine, board, depth=20, multipv=2, update_interval=2)
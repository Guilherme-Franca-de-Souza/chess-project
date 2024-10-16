import random
import chess
import chess.engine
import StaticEvaluatorRN
from functools import lru_cache

nodes_evaluated = 0
transposition_table = {}

@lru_cache(maxsize=None)
def evaluate_board(board_fen):
    board = chess.Board(board_fen)
    return evaluator.evaluate(board)

def evaluate_move(board, move):
    board.push(move)
    evaluation = evaluate_board(board.fen())
    board.pop()
    return evaluation

def minimax(board, depth, alpha, beta, maximizing_player):
    global nodes_evaluated
    board_fen = board.fen()

    if board_fen in transposition_table:
        return transposition_table[board_fen]

    nodes_evaluated += 1

    if board.is_checkmate():
        return 9999999999 if maximizing_player else -9999999999
    if board.is_stalemate() or board.is_insufficient_material() or board.is_seventyfive_moves() or board.is_fivefold_repetition():
        return 0  # Empate

    if depth == 0:
        return random.randint(-100, 100)

    legal_moves = list(board.legal_moves)
    # Avalie e ordene os movimentos por uma heurística simples
    legal_moves.sort(key=lambda move: evaluate_move(board, move), reverse=maximizing_player)

    if maximizing_player:
        max_eval = float('-inf')
        for move in legal_moves:
            board.push(move)
            eval = minimax(board, depth - 1, alpha, beta, False)
            board.pop()
            max_eval = max(max_eval, eval)
            alpha = max(alpha, eval)
            if beta <= alpha:
                break  # Poda beta
        transposition_table[board_fen] = max_eval
        return max_eval
    else:
        min_eval = float('inf')
        for move in legal_moves:
            board.push(move)
            eval = minimax(board, depth - 1, alpha, beta, True)
            board.pop()
            min_eval = min(min_eval, eval)
            beta = min(beta, eval)
            if beta <= alpha:
                break  # Poda alfa
        transposition_table[board_fen] = min_eval
        return min_eval

def find_best_move(board, depth):
    global nodes_evaluated
    best_move = None
    best_eval = float('-inf')
    alpha = float('-inf')
    beta = float('inf')

    legal_moves = list(board.legal_moves)
    # Avaliar e ordenar os movimentos antes de começar a busca
    legal_moves.sort(key=lambda move: evaluate_move(board, move), reverse=True)

    for move in legal_moves:
        board.push(move)
        current_eval = minimax(board, depth - 1, alpha, beta, False)
        board.pop()

        if current_eval > best_eval:
            best_eval = current_eval
            best_move = move

    print(f"Nós avaliados: {nodes_evaluated}")
    nodes_evaluated = 0  # Reset para a próxima busca
    return best_move

def main():
    global evaluator
    engine = chess.engine.SimpleEngine.popen_uci("/usr/games/stockfish")
    evaluator = StaticEvaluatorRN.StaticEvaluatorRN()

    board = chess.Board()
    depth = 4  # Aumente a profundidade máxima conforme necessário

    while not board.is_game_over():
        print(board)
        if board.turn == chess.WHITE:
            best_move = find_best_move(board, depth)
            print(f"Melhor lance para as brancas: {best_move}")
        else:
            best_move = engine.play(board, chess.engine.Limit(depth=1)).move
            print(f"Melhor lance para as negras: {best_move}")

        board.push(best_move)

    print("Jogo terminado!")
    engine.quit()

if __name__ == "__main__":
    main()
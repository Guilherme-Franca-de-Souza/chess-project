import chess
import chess.engine
import StaticEvaluatorRN
from functools import lru_cache
from concurrent.futures import ThreadPoolExecutor, as_completed

nodes_evaluated = 0
transposition_table = {}

@lru_cache(maxsize=None)
def evaluate_board(board_fen):
    global count
    count += 1
    #print(count)
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
        return evaluate_board(board_fen)

    legal_moves = list(board.legal_moves)
    # Avalie e ordene os movimentos por uma heurística simples
    legal_moves.sort(key=lambda move: evaluate_move(board, move), reverse=maximizing_player)

    if maximizing_player:
        max_eval = float('-inf')
        with ThreadPoolExecutor() as executor:
            futures = {
                executor.submit(evaluate_minimax, board.copy(), move, depth, alpha, beta, False): move
                for move in legal_moves
            }
            for future in as_completed(futures):
                eval = future.result()
                max_eval = max(max_eval, eval)
                alpha = max(alpha, eval)
                if beta <= alpha:
                    break  # Poda beta
        transposition_table[board_fen] = max_eval
        return max_eval
    else:
        min_eval = float('inf')
        with ThreadPoolExecutor() as executor:
            futures = {
                executor.submit(evaluate_minimax, board.copy(), move, depth, alpha, beta, True): move
                for move in legal_moves
            }
            for future in as_completed(futures):
                eval = future.result()
                min_eval = min(min_eval, eval)
                beta = min(beta, eval)
                if beta <= alpha:
                    break  # Poda alfa
        transposition_table[board_fen] = min_eval
        return min_eval

def evaluate_minimax(board, move, depth, alpha, beta, maximizing_player):
    board.push(move)
    eval = minimax(board, depth - 1, alpha, beta, maximizing_player)
    board.pop()
    return eval

def find_best_move(board, depth):
    global nodes_evaluated
    best_move = None
    best_eval = float('-inf')
    alpha = float('-inf')
    beta = float('inf')

    legal_moves = list(board.legal_moves)
    legal_moves.sort(key=lambda move: evaluate_move(board, move), reverse=True)

    with ThreadPoolExecutor() as executor:
        futures = {
            executor.submit(evaluate_minimax, board.copy(), move, depth, alpha, beta, False): move
            for move in legal_moves
        }
        for future in as_completed(futures):
            current_eval = future.result()
            move = futures[future]

            if current_eval > best_eval:
                best_eval = current_eval
                best_move = move

    print(f"Nós avaliados: {nodes_evaluated}")
    nodes_evaluated = 0  # Reset para a próxima busca
    return best_move

def main():
    global evaluator
    global count
    count = 0
    engine = chess.engine.SimpleEngine.popen_uci("/usr/games/stockfish")
    evaluator = StaticEvaluatorRN.StaticEvaluatorRN()

    board = chess.Board()
    depth = 3 # Aumente a profundidade máxima conforme necessário

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

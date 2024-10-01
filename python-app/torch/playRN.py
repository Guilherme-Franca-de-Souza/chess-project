import chess
import chess.engine
import StaticEvaluatorRN

def minimax(board, depth, alpha, beta, maximizing_player, evaluator):
    if board.is_checkmate():
        return 9999999999 if maximizing_player else -9999999999
    if board.is_stalemate() or board.is_insufficient_material() or board.is_seventyfive_moves() or board.is_fivefold_repetition():
        return 0  # Empate

    if depth == 0:
        return evaluator.evaluate(board)

    if maximizing_player:
        max_eval = float('-inf')
        for move in board.legal_moves:
            board.push(move)
            eval = minimax(board, depth - 1, alpha, beta, False, evaluator)
            board.pop()
            max_eval = max(max_eval, eval)
            alpha = max(alpha, eval)
            if beta <= alpha:
                break  # Poda beta
        return max_eval
    else:
        min_eval = float('inf')
        for move in board.legal_moves:
            board.push(move)
            eval = minimax(board, depth - 1, alpha, beta, True, evaluator)
            board.pop()
            min_eval = min(min_eval, eval)
            beta = min(beta, eval)
            if beta <= alpha:
                break  # Poda alfa
        return min_eval

def find_best_move(board, depth, evaluator):
    best_move = None
    best_eval = float('-inf')
    alpha = float('-inf')
    beta = float('inf')

    for move in board.legal_moves:
        board.push(move)
        current_eval = minimax(board, depth - 1, alpha, beta, False, evaluator)
        board.pop()

        if current_eval > best_eval:
            best_eval = current_eval
            best_move = move

    return best_move

def main():
    engine = chess.engine.SimpleEngine.popen_uci("/usr/games/stockfish")
    evaluator = StaticEvaluatorRN.StaticEvaluatorRN()

    board = chess.Board()
    depth = 2  # Profundidade máxima

    while not board.is_game_over():
        print(board)
        if board.turn == chess.WHITE:
            best_move = find_best_move(board, depth, evaluator)
            print(f"Melhor lance para as brancas: {best_move}")
        else:
            best_move = engine.play(board, chess.engine.Limit(depth=1)).move
            print(f"Melhor lance para as negras: {best_move}")

        board.push(best_move)

    print("Jogo terminado!")
    engine.quit()

if __name__ == "__main__":
    main()
import chess
import chess.engine

# Substitua isso pela sua função de avaliação estática
def static_evaluation(board):
    # Exemplo de função de avaliação estática (substitua pela sua)
    return sum(piece_value(piece) for piece in board.piece_map().values())

def piece_value(piece):
    values = {
        chess.PAWN: 1,
        chess.KNIGHT: 3,
        chess.BISHOP: 3,
        chess.ROOK: 5,
        chess.QUEEN: 9,
        chess.KING: 0
    }
    return values.get(piece.piece_type, 0)

def is_check_or_mate(board):
    return board.is_check() or board.is_checkmate()

def minimax(board, depth, maximizing_player, engine):
    if depth == 0 or is_check_or_mate(board):
        return static_evaluation(board)

    if maximizing_player:
        max_eval = float('-inf')
        for move in board.legal_moves:
            board.push(move)
            eval = minimax(board, depth - 1, False, engine)
            board.pop()
            max_eval = max(max_eval, eval)
        return max_eval
    else:
        min_eval = float('inf')
        for move in board.legal_moves:
            board.push(move)
            eval = minimax(board, depth - 1, True, engine)
            board.pop()
            min_eval = min(min_eval, eval)
        return min_eval

def find_best_move(board, depth, engine):
    best_move = None
    best_eval = float('-inf')

    for move in board.legal_moves:
        board.push(move)
        current_eval = minimax(board, depth - 1, False, engine)
        board.pop()

        if current_eval > best_eval:
            best_eval = current_eval
            best_move = move

    return best_move

def main():
    # Inicie o Stockfish (substitua o caminho para o executável Stockfish)
    engine = chess.engine.SimpleEngine.popen_uci("path/to/stockfish")

    board = chess.Board()
    depth = 5  # Profundidade máxima

    while not board.is_game_over():
        print(board)
        if board.turn == chess.WHITE:
            best_move = find_best_move(board, depth, engine)
            print(f"Melhor lance para as brancas: {best_move}")
        else:
            # As negras também jogam usando o Stockfish
            best_move = engine.play(board, chess.engine.Limit(time=2.0)).move
            print(f"Melhor lance para as negras: {best_move}")

        board.push(best_move)

    print("Jogo terminado!")
    engine.quit()

if __name__ == "__main__":
    main()
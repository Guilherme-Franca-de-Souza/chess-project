import chess
import chess.pgn
import chess.engine

# Define the engine path
engine_path = "/usr/local/bin/stockfish"

# Initialize engines
classical = chess.engine.SimpleEngine.popen_uci(engine_path)
classical.configure({"Use NNUE": False})

nnue = chess.engine.SimpleEngine.popen_uci(engine_path)

# Function to play a game
def play_game(white_engine, black_engine, depth_limit, time_limit):
    board = chess.Board()
    game = chess.pgn.Game()
    game.headers["White"] = "Classical" if white_engine == classical else "NNUE"
    game.headers["Black"] = "NNUE" if black_engine == nnue else "Classical"
    
    node = game
    while not board.is_game_over():
        result = white_engine.play(board, chess.engine.Limit(time=time_limit,depth=depth_limit))
        board.push(result.move)
        node = node.add_variation(result.move)
        if board.is_game_over():
            break
        result = black_engine.play(board, chess.engine.Limit(time=time_limit,depth=depth_limit))
        board.push(result.move)
        node = node.add_variation(result.move)
    
    game.headers["Result"] = board.result()
    return game

# Play both games
depth_limit = 2  # Limit the depth to 2
time_limit = 10
game1 = play_game(classical, nnue, depth_limit, time_limit)
game2 = play_game(nnue, classical, depth_limit, time_limit)

# Save games to PGN
with open("game1.pgn", "w") as f:
    f.write(str(game1))

with open("game2.pgn", "w") as f:
    f.write(str(game2))

# Close engines
classical.quit()
nnue.quit()
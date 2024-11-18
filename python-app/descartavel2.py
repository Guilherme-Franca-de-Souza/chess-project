import chess.engine

# Caminho para o executável do Stockfish
stockfish_15 = "/usr/games/stockfish" 

stockfish_16 = "/usr/local/bin/sf16/stockfish" 

stockfish_17 = "/usr/local/bin/sf17/stockfish"

# Inicia o motor Stockfish
with chess.engine.SimpleEngine.popen_uci(stockfish_15) as engine:
    # Solicita a versão do motor Stockfish
    print(f"Versão do Stockfish 16: {engine.id}")


# Inicia o motor Stockfish
with chess.engine.SimpleEngine.popen_uci(stockfish_16) as engine:
    # Solicita a versão do motor Stockfish
    print(f"Versão do Stockfish 16: {engine.id}")

# Inicia o motor Stockfish
with chess.engine.SimpleEngine.popen_uci(stockfish_17) as engine:
    # Solicita a versão do motor Stockfish
    print(f"Versão do Stockfish 17: {engine.id}")
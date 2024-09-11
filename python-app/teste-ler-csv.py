import csv
import io
import chess
import chess.pgn
import chess.engine

# Configura o caminho para o executável do Stockfish
STOCKFISH_PATH = '/caminho/para/stockfish'

# Função para ler o conteúdo do CSV
def read_csv(file_path):
    with open(file_path, mode='r', newline='', encoding='utf-8') as file:
        reader = csv.reader(file)
        next(reader)  # Pular o cabeçalho
        for row in reader:
            file_name, pgn_content = row
            yield pgn_content

# Função para analisar o conteúdo PGN com Stockfish e obter o FEN de todas as posições
def analyze_pgn(pgn_content):
    board = chess.Board()
    game = chess.pgn.read_game(io.StringIO(pgn_content))
    for move in game.mainline_moves():
        board.push(move)
        print(f"FEN após o movimento {move}: {board.fen()}")

# Caminho para o arquivo CSV
csv_file_path = 'games.csv'

# Ler o conteúdo PGN do CSV e analisar com Stockfish
for pgn_content in read_csv(csv_file_path):
    print("Analisando jogo...")
    analyze_pgn(pgn_content)
    print("\n")

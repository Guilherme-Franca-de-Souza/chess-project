import os
from chess import pgn
from tqdm import tqdm
import csv

#files = [file for file in os.listdir("pgns") if file.endswith(".pgn")]
file_name = "lichess_elite_2013-09.pgn"

def load_pgn(file_path):
    games = []
    i = 0
    with open(file_path, 'r') as pgn_file:
        while True:
            game = pgn.read_game(pgn_file)
            i += 1
            print(i)
            if game is None:
                break
            games.append(game)
    return games

games = []
i = 1
#for file in files:
#name = file
games.extend(load_pgn(f"pgns/{file_name}")) ## pgns/file

def game_to_pgn_string(game):
    return game.accept(pgn.StringExporter())

# Preparar os dados para o CSV
csv_data = [["PGN Id", "PGN Content"]]
for i, game in enumerate(games, 1):
    pgn_content = game_to_pgn_string(game)
    csv_data.append([f"{file_name}_{i}.pgn", pgn_content]) ## {file}_

# Escrever o arquivo CSV
with open('games.csv', mode='w', newline='', encoding='utf-8') as file:
    writer = csv.writer(file)
    writer.writerows(csv_data)

print("Arquivo CSV criado com sucesso!")

print(games)

import os
from chess import pgn
import csv

files = [file for file in os.listdir("pgns") if file.endswith(".pgn")]
#files = ["lichess_elite_2013-09.pgn", "lichess_elite_2014-04.pgn", "lichess_elite_2013-11.pgn"]

def load_pgn(file_path, total_games, arquivo_atual, total_arquivos):
    games = []
    i = 0
    with open(file_path, 'r') as pgn_file:
        while True:
            game = pgn.read_game(pgn_file)
            i += 1
            os.system('clear')
            print(arquivo_atual, '//', total_arquivos, ' ::: ', i, ' / ', total_games, '  ->', pgn_file.name)
            if game is None:
                break
            games.append(game)
    return games

def game_to_pgn_string(game):
    return game.accept(pgn.StringExporter())

games = []

total_files = len(files)
for index, file in enumerate(files, start=1):

    count = 1
    with open(f"pgns/{file}", 'r') as pgn_file:
        for line in pgn_file:
            if line.startswith("[Event"):
                count += 1

    games.extend(load_pgn(f"pgns/{file}", count, index, total_files))

    # Preparar os dados para o CSV
    csv_data = []
    for i, game in enumerate(games, 1):
        pgn_content = game_to_pgn_string(game)
        csv_data.append([f"{file}_{i}", pgn_content])

    # Escrever no arquivo CSV em modo de append
    with open('games.csv', mode='a', newline='', encoding='utf-8') as csv_file:
        writer = csv.writer(csv_file)
        if index == 1:  # Escrever o cabeçalho apenas no primeiro arquivo
            writer.writerow(["PGN_Id", "PGN_Content"])
        writer.writerows(csv_data)

    # Limpar a lista de jogos processados
    games.clear()

print("Arquivo CSV criado com sucesso!")
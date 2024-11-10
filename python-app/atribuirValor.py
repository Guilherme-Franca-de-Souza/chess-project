import csv
import StockfishEngineEval
import random
from itertools import islice

def adicionar_avaliacoes(input_file, output_file):
    with open(input_file, 'r') as infile, open(output_file, 'w', newline='') as outfile:
        reader = csv.reader(infile)
        writer = csv.writer(outfile)

         # Ignora as primeiras 50 milhões de linhas
        reader = islice(reader, 50000000, None)
        
        # Escreve o header
        writer.writerow(["FEN", "avaliacao", "avaliacao17"])
        
        # Processa linha por linha
        i = 0
        for row in reader:
            i += 1
            print(i)
            if (i > 2500000):
                break
            fen = row[0]
            avaliacao = row[1]
            avaliacao17 = StockfishEngineEval.eval(row[0])
            try:
                avaliacao17 = float(avaliacao17)
                writer.writerow([fen, avaliacao, avaliacao17])
            except ValueError:
                pass

# Exemplo de uso
input_file = 'avaliacoes-01.csv'
output_file = 'avaliacoes.csv'
adicionar_avaliacoes(input_file, output_file)
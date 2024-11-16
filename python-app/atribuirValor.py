import csv
import StockfishEngineEval
import random
from itertools import islice

def adicionar_avaliacoes(input_file, output_file):
    with open(input_file, 'r') as infile, open(output_file, 'w', newline='') as outfile:
        reader = csv.reader(infile)
        writer = csv.writer(outfile)

        # Ignora as primeiras 50 milhões de linhas
        reader = islice(reader, 1, None)
        
        # Escreve o header
        writer.writerow(["FEN", "avaliacao", "avaliacao17", "avaliacao16"])
        
        # Processa linha por linha
        i = 0
        for row in reader:
            i += 1
            print(i)
            if (i > 20000):
                break
            fen = row[0]
            avaliacao = row[1]
            avaliacao17 = row[2]
            avaliacao16 = StockfishEngineEval.eval(row[0])
            try:
                avaliacao16 = float(avaliacao16)
                writer.writerow([fen, avaliacao, avaliacao17, avaliacao16])
            except ValueError:
                pass

# Exemplo de uso
input_file = 'avaliacoes.csv'
output_file = 'avaliacoes-15-16-17.csv'
adicionar_avaliacoes(input_file, output_file)
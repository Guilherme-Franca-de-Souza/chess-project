import csv
import StockfishEngineEval
import random

def adicionar_avaliacoes(input_file, output_file):
    with open(input_file, 'r') as infile, open(output_file, 'w', newline='') as outfile:
        reader = csv.reader(infile)
        writer = csv.writer(outfile)

        next(infile)
        next(infile)
        
        # Escreve o header
        #writer.writerow(["FEN", "avaliação"])
        
        # Processa linha por linha
        for row in reader:
            fen = row[0]
            print(row[0])
            print(StockfishEngineEval.eval(row[0]))
            #avaliacao = calcular_avaliacao(fen)
            #writer.writerow([fen, avaliacao])

# Exemplo de uso
input_file = 'fens/fens-games-01.csv'
output_file = 'avaliacoes-01.csv'
adicionar_avaliacoes(input_file, output_file)
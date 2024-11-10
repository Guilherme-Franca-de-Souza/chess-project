import csv

def criar_csv_pequeno(arquivo_entrada, arquivo_saida, pular=30000000, linhas=10000):
    with open(arquivo_entrada, 'r') as infile, open(arquivo_saida, 'w', newline='') as outfile:
        reader = csv.reader(infile)
        writer = csv.writer(outfile)

        # Ignora as primeiras 'pular' linhas
        for _ in range(pular):
            next(reader, None)  # Usa None para ignorar o fim do arquivo se for menor que 10 linhas

        # Copia as próximas 'linhas' linhas
        for i, row in enumerate(reader):
            print(i)
            if i < linhas:
                writer.writerow(row)
            else:
                break

# Exemplo de uso
arquivo_entrada = 'avaliacoes-01.csv'
arquivo_saida = 'amostras.csv'
criar_csv_pequeno(arquivo_entrada, arquivo_saida)

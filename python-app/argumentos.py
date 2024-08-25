import argparse

# Cria o parser
parser = argparse.ArgumentParser(description='Recebe duas variáveis.')

# Define os argumentos esperados
parser.add_argument('var1', type=str, help='Primeira variável')
parser.add_argument('var2', type=str, help='Segunda variável')

# Faz o parsing dos argumentos
args = parser.parse_args()

# Acessa os valores das variáveis
print(f"Variável 1: {args.var1}")
print(f"Variável 2: {args.var2}")
import mysql.connector
import pandas as pd
import matplotlib.pyplot as plt
import matplotlib.patches as mpatches

# Configurar conexão ao banco de dados MySQL
conn = mysql.connector.connect(
    host='db', 
    user='root', 
    password='password', 
    database='chess'
)

# Consultar dados dos jogadores e das partidas
query_jogadores = "SELECT id, nome, profundidade, redes_neurais FROM jogadores"
query_partidas = "SELECT brancas_id, negras_id, vencedor_id FROM partidas"

df_jogadores = pd.read_sql(query_jogadores, conn)
df_partidas = pd.read_sql(query_partidas, conn)

# Separar jogadores por time
jogadores_time0 = df_jogadores[df_jogadores['redes_neurais'] == 0]['id'].tolist()
jogadores_time1 = df_jogadores[df_jogadores['redes_neurais'] == 1]['id'].tolist()

# Criar uma tabela vazia para armazenar os resultados
tabela = pd.DataFrame(index=jogadores_time0, columns=jogadores_time1, dtype=object)

# Preencher a tabela com listas vazias
for time0 in jogadores_time0:
    for time1 in jogadores_time1:
        tabela.at[time0, time1] = ['', '']

# Preencher a tabela com resultados
for _, partida in df_partidas.iterrows():
    jogador_brancas = partida['brancas_id']
    jogador_negras = partida['negras_id']
    vencedor = partida['vencedor_id']

    if jogador_brancas in jogadores_time1 and jogador_negras in jogadores_time0:
        time1 = jogador_brancas
        time0 = jogador_negras
        
        # Se a célula estiver vazia, inicialize-a com uma lista de duas posições
        if tabela.at[time0, time1] == ['', '']:
            tabela.at[time0, time1] = ['', '']
        
        if vencedor == time1:
            tabela.at[time0, time1][0] = 'T1'  # Time 1 venceu (amarelo)
        elif vencedor == time0:
            tabela.at[time0, time1][0] = 'T0'  # Time 0 venceu (rosa)
        else:
            tabela.at[time0, time1][0] = 'E'  # Empate (branco)

    elif jogador_brancas in jogadores_time0 and jogador_negras in jogadores_time1:
        time0 = jogador_brancas
        time1 = jogador_negras

        # Se a célula estiver vazia, inicialize-a com uma lista de duas posições
        if tabela.at[time0, time1] == ['', '']:
            tabela.at[time0, time1] = ['', '']
        
        if vencedor == time1:
            tabela.at[time0, time1][1] = 'T1'  # Time 1 venceu (amarelo)
        elif vencedor == time0:
            tabela.at[time0, time1][1] = 'T0'  # Time 0 venceu (rosa)
        else:
            tabela.at[time0, time1][1] = 'E'  # Empate (branco)

# Função para colorir as células
def colorir_celula(plt, x, y, resultado1, resultado2):
    colors = {'T0': 'pink', 'T1': 'yellow', 'E': 'white'}
    plt.fill_between([x, x + 1], [y, y], [y + 0.5, y + 0.5], color=colors[resultado1])
    plt.fill_between([x, x + 1], [y + 0.5, y + 0.5], [y + 1, y + 1], color=colors[resultado2])

# Configurar o gráfico
fig, ax = plt.subplots(figsize=(10, 10))

# Desenhar a tabela de resultados
for i, jogador_time0 in enumerate(jogadores_time0):
    for j, jogador_time1 in enumerate(jogadores_time1):
        # Se a célula não estiver vazia, desenhar os resultados
        if tabela.at[jogador_time0, jogador_time1] != ['', '']:
            resultado1, resultado2 = tabela.at[jogador_time0, jogador_time1]
            colorir_celula(ax, j, i, resultado1, resultado2)

# Ajustar o gráfico
ax.set_xticks([i + 0.5 for i in range(len(jogadores_time1))])
ax.set_yticks([i + 0.5 for i in range(len(jogadores_time0))])
ax.set_xticklabels(jogadores_time1)
ax.set_yticklabels(jogadores_time0)
ax.invert_yaxis()

ax.spines['top'].set_visible(True)  # Visível
ax.spines['bottom'].set_visible(True)
ax.spines['left'].set_visible(True)
ax.spines['right'].set_visible(True)

# Legenda
#rosa_patch = mpatches.Patch(color='pink', label='Time 0 Venceu')
#amarelo_patch = mpatches.Patch(color='yellow', label='Time 1 Venceu')
#empate_patch = mpatches.Patch(color='white', label='Empate')
#plt.legend(handles=[rosa_patch, amarelo_patch, empate_patch], loc='upper right')

# Exibir o gráfico
plt.savefig('resultado_partidas.png')

# Fechar conexão com o banco de dados
conn.close()
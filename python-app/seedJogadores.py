from models import Jogador
import os
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker

DB_USER = os.getenv("DB_USER", "root")
DB_PASSWORD = os.getenv("DB_PASSWORD", "password")
DB_HOST = os.getenv("DB_HOST", "db")
DB_NAME = os.getenv("DB_NAME", "chess")
DATABASE_URL = f"mysql+mysqlconnector://{DB_USER}:{DB_PASSWORD}@{DB_HOST}/{DB_NAME}"
engine = create_engine(DATABASE_URL)
Session = sessionmaker(bind=engine)
session = Session()

# Criando 20 jogadores com redes_neurais = 0 e profundidade de 1 a 20
for profundidade in range(1, 21):
    jogador = Jogador()
    jogador.nome = f"Stockfish - P {profundidade} - RN 0"
    jogador.profundidade = profundidade
    jogador.redes_neurais = 0
    session.add(jogador)

# Criando 20 jogadores com redes_neurais = 1 e profundidade de 1 a 20
for profundidade in range(1, 21):
    jogador = Jogador()
    jogador.nome = f"Stockfish - P {profundidade} - RN 1"
    jogador.profundidade = profundidade
    jogador.redes_neurais = 1
    session.add(jogador)

# Commit para salvar todos os jogadores no banco de dados
session.commit()

print("Seed de jogadores concluída com sucesso.")

import chess
import chess.engine
import random
import os
from sqlalchemy import create_engine
from sqlalchemy import or_, and_
from sqlalchemy.orm import sessionmaker
from models import Base, Posicao, Partida, Jogador, Avaliacao, Cenario, Ambiente
from eval import eval
import time
import argparse

#captura argumentos
parser = argparse.ArgumentParser(description='Recebe duas variáveis.')
parser.add_argument('profundidadeEngineComRedesNeurais', type=str, help='Profundidade da engine com redes neurais')
parser.add_argument('profundidadeEngineSemRedesNeurais', type=str, help='Profundidade da engine sem redes neurais')
args = parser.parse_args()

# Define o path da engine
engine_path = "/usr/games/stockfish"

# Conexão com o MySQL via SQLAlchemy
def create_connection():
    DB_USER = os.getenv("DB_USER", "root")
    DB_PASSWORD = os.getenv("DB_PASSWORD", "password")
    DB_HOST = os.getenv("DB_HOST", "db")
    DB_NAME = os.getenv("DB_NAME", "chess")
    DATABASE_URL = f"mysql+mysqlconnector://{DB_USER}:{DB_PASSWORD}@{DB_HOST}/{DB_NAME}"
    engine = create_engine(DATABASE_URL)
    Session = sessionmaker(bind=engine)
    return Session()


# Aparentemente o stockfish guarda em cache avaliações de uma posição
# então se eu chamar essa função várias vezes para a mesma posição
# Ele vai sempre melhorar a análise
def get_best_lines(engine, board, depth=20, multipv=1):
    info = engine.analyse(board, chess.engine.Limit(depth=depth), multipv=multipv)
    return info

# Mostra as linhas de uma forma menos poluida
def get_line_str(line):
    line_str = ', '.join([move.uci() for move in line])
    return line_str

def main(profundidadeEngineComRedesNeurais, profundidadeEngineSemRedesNeurais):
    session = create_connection()
    # Busca os jogadores no banco
    jogadorComRedesNeurais = session.query(Jogador).filter(and_(
            Jogador.profundidade == profundidadeEngineComRedesNeurais,
            Jogador.redes_neurais == 1
        )).first()
    jogadorSemRedesNeurais = session.query(Jogador).filter(and_(
            Jogador.profundidade == profundidadeEngineSemRedesNeurais,
            Jogador.redes_neurais == 0
        )).first()

    print(jogadorComRedesNeurais.nome, jogadorSemRedesNeurais.nome)

    #classical = chess.engine.SimpleEngine.popen_uci(engine_path)
    #classical.configure({"Use NNUE": False})

    #nnue = chess.engine.SimpleEngine.popen_uci(engine_path)
    """    
    fen = '8/3K3B/4p2P/2p1k1p1/8/p7/8/8 w - - 0 1'
    board = chess.Board(fen)
    try:
        while True:
            classical_best_lines = get_best_lines(classical, board, depth=3)
            for i, line_info in enumerate(classical_best_lines):
                print('\n\n')
                score = line_info['score'].relative.score(mate_score=10000)
                #line = line_info['pv']
                #line_str = get_line_str(line) 
                print(f"Classical Score = {score}")
            nnue_best_lines = get_best_lines(nnue, board, depth=3)
            for i, line_info in enumerate(nnue_best_lines):
                print('\n\n')
                score = line_info['score'].relative.score(mate_score=10000)
                #line = line_info['pv']
                #line_str = get_line_str(line) 
                print(f"NNUE Score = {score}")
            another_best_lines = get_best_lines(another, board, depth=3)
            for i, line_info in enumerate(another_best_lines):
                print('\n\n')
                score = line_info['score'].relative.score(mate_score=10000)
                #line = line_info['pv']
                #line_str = get_line_str(line) 
                print(f"NNUE Score = {score}")
            
        
            time.sleep(1)
    except Exception as e:
        print(f"Engine error: {e} ")
    """
    

if __name__ == "__main__":
    main(args.profundidadeEngineComRedesNeurais, args.profundidadeEngineSemRedesNeurais)
    #classical.quit()
    #nnue.quit()
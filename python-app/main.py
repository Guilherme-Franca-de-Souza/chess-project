import chess
import chess.engine
import random
import os
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from models import Base, Posicao, Sequencia
import time


# Inicia o stockfish com o path de dentro dentro do container
engine_path = "/usr/games/stockfish"
engine = chess.engine.SimpleEngine.popen_uci(engine_path)

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

# cria um FEN válido aleatório
def get_random_fen(): ## ACHO QUE NÃO VOU UTILIZAR
    board = chess.Board()
    for _ in range(random.randint(1, 20)):
        move = random.choice(list(board.legal_moves))
        board.push(move)
    return board.fen()


# Aparentemente o stockfish guarda em cache avaliações de uma posição
# então se eu chamar essa função várias vezes para a mesma posição
# Ele vai sempre melhorar a análise
def get_best_lines(board, depth=20, multipv=3):
    info = engine.analyse(board, chess.engine.Limit(depth=depth), multipv=multipv)
    return info

# Mostra as linhas de uma forma menos poluida
def get_line_str(line):
    line_str = ', '.join([move.uci() for move in line])
    return line_str

def main():
    #session = create_connection()
    #Base.metadata.create_all(session.get_bind())  # Cria as tabelas, se não existirem

    fen = '8/3K3B/4p2P/2p1k1p1/8/p7/8/8 w - - 0 30'
    board = chess.Board(fen)
    try:
        while True:
            best_lines = get_best_lines(board, depth=20)
            for i, line_info in enumerate(best_lines):
                print('\n\n')
                score = line_info['score'].relative.score(mate_score=10000)
                line = line_info['pv']
                line_str = get_line_str(line) 
                print(f"Line {i+1}: Score = {score}, Moves = {line_str} ")
        
            time.sleep(1)
    except Exception as e:
        print(f"Engine error: {e} ")

if __name__ == "__main__":
    main()
    engine.quit()
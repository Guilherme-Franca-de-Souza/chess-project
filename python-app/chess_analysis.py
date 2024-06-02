import chess
import chess.engine
import random
import os
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from models import Base, PosicaoInicial, Sequencia

# Configuração do Stockfish
engine = chess.engine.SimpleEngine.popen_uci("/usr/games/stockfish")

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

def get_random_fen():
    board = chess.Board()
    for _ in range(random.randint(1, 20)):
        move = random.choice(list(board.legal_moves))
        board.push(move)
    return board.fen()

def evaluate_position(fen):
    board = chess.Board(fen)
    result = engine.analyse(board, chess.engine.Limit(time=60))
    return result['score'].relative.score()

def main():
    session = create_connection()
    Base.metadata.create_all(session.get_bind())  # Cria as tabelas, se não existirem

    random_fen = get_random_fen()
    initial_evaluation = evaluate_position(random_fen)
    print(initial_evaluation)
    
    # Inserir posição inicial
    posicao_inicial = PosicaoInicial(fen=random_fen, avaliacao=initial_evaluation)
    session.add(posicao_inicial)
    session.commit()

    # Gerar sequências
    board = chess.Board(random_fen)
    for move in board.legal_moves:
        board.push(move)
        fen = board.fen()
        evaluation = evaluate_position(fen)
        sequencia = Sequencia(id_posicao_inicial=posicao_inicial.id, fen=fen, avaliacao=evaluation)
        session.add(sequencia)
        session.commit()
        board.pop()

if __name__ == "__main__":
    main()
    engine.quit()
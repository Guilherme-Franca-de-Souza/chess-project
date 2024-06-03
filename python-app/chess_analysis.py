import chess
import chess.engine
import random
import os
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from models import Base, Posicao, Sequencia

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
    result = engine.analyse(board, chess.engine.Limit(time=240, depth=240))
    #return result['score'].relative.score()
    return result

def main():
    #session = create_connection()
    #Base.metadata.create_all(session.get_bind())  # Cria as tabelas, se não existirem

    fen = '8/3K3B/4p2P/2p1k1p1/8/p7/8/8 w - - 0 30'
    try:
        #fen = 'r1bq3k/ppp1nQp1/4pN1p/6N1/2BP4/2P1n3/PP4PP/R5K1 w - - 0 30'
        evaluation = evaluate_position(fen)
        pv_moves = evaluation['pv']
        best_moves = [move.uci() for move in pv_moves]

        print(best_moves)
        
        #print("Best sequence of moves:", evaluation)
    except chess.engine.EngineError as e:
        print(f"Engine error: {e}")

    '''
    random_fen = get_random_fen()
    initial_evaluation = evaluate_position(random_fen)
    print(initial_evaluation)
    
    # Inserir posição inicial
    posicao = Posicao(fen=random_fen, avaliacao=initial_evaluation)
    session.add(posicao)
    session.commit()

    # Gerar sequências
    board = chess.Board(random_fen)
    for move in board.legal_moves:
        board.push(move)
        fen = board.fen()
        evaluation = evaluate_position(fen)
        sequencia = Sequencia(id_posicao=posicao.id, fen=fen, avaliacao=evaluation)
        session.add(sequencia)
        session.commit()
        board.pop()
    '''

if __name__ == "__main__":
    main()
    engine.quit()
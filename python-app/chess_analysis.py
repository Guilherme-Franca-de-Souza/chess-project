import chess
import chess.engine
import random
import os
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from models import Base, Posicao, Sequencia
import time


# Configuração do Stockfish
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

def get_best_lines(board, depth=10):
    info = engine.analyse(board, chess.engine.Limit(depth=depth), multipv=3)
    return info

def main():
    #session = create_connection()
    #Base.metadata.create_all(session.get_bind())  # Cria as tabelas, se não existirem

    fen = '8/3K3B/4p2P/2p1k1p1/8/p7/8/8 w - - 0 30'
    board = chess.Board(fen)

    with chess.engine.SimpleEngine.popen_uci(engine_path) as engine:
        # Defina parâmetros para uma avaliação rápida
        options = {
            'Threads': 1,
            'Hash': 16,  # Use um valor baixo para memória de hash
            'Skill Level': 0,  # Nível de habilidade mínimo
        }
        for option, value in options.items():
            engine.configure({option: value})
        
        # Envie o comando de análise com profundidade mínima
        limit = chess.engine.Limit(depth=1, time=0.1)  # Configuração de tempo curto para reduzir a análise
        
        eval_info = engine.analyse(board, limit)

        # Obtenha a avaliação estática
        eval_score = eval_info['score'].relative.score(mate_score=100000)  # Utilize um score alto para cheques-mate
        print(eval_info)

    '''
    try:
        fen = '8/3K3B/4p2P/2p1k1p1/8/p7/8/8 w - - 0 30'
        board = chess.Board(fen)

        eval_info = engine.analyse(board, chess.engine.Limit(depth=0))

        print(eval_info)
    except Exception as e:
        print(e)

     try:
        fen = '8/3K3B/4p2P/2p1k1p1/8/p7/8/8 w - - 0 30'
        board = chess.Board(fen)

        best_lines = get_best_lines(board, depth=10)
        for i, line_info in enumerate(best_lines):
            score = line_info['score'].relative.score(mate_score=10000)
            line = line_info['pv']
            line_str = " ".join([board.san(move) for move in line])
            print(f"Line {i+1}: Score = {score}, Moves = {line_str}")
    except Exception as e:
        print(f"Engine error: {e} ")

    try:
        #fen = 'r1bq3k/ppp1nQp1/4pN1p/6N1/2BP4/2P1n3/PP4PP/R5K1 w - - 0 30'
        evaluation = evaluate_position(fen)
        pv_moves = evaluation['pv']
        best_moves = [move.uci() for move in pv_moves]
        print(best_moves)
        
        #print("Best sequence of moves:", evaluation)
    except chess.engine.EngineError as e:
        print(f"Engine error: {e}")

    
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
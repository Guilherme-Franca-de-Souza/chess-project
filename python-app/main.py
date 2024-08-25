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

def play_game(jogador_brancas, jogador_negras, cenario):
    fen = cenario.fen
    board = chess.Board(fen)

    engineBrancas = chess.engine.SimpleEngine.popen_uci(engine_path) 
    if (jogador_brancas.redes_neurais == 0) {
        engineBrancas.configure({"Use NNUE": False})
    }

    engineNegras = chess.engine.SimpleEngine.popen_uci(engine_path) 
    if (jogador_negras.redes_neurais == 0) {
        engineBrancas.configure({"Use NNUE": False})
    }

    brancas = {
        'engine': engineBrancas
        'dados': jogador_brancas
    }

    negras = {
        'engine': engineNegras
        'dados': jogador_negras
    }

    game = chess.pgn.Game()
    game.headers["White"] = brancas['dados'].nome
    game.headers["Black"] = negras['dados'].nome
    
    node = game
    while not board.is_game_over():
        result = brancas['engine'].play(board, chess.engine.Limit(depth=brancas['dados'].profundidade))
        board.push(result.move)
        node = node.add_variation(result.move)
        if board.is_game_over():
            break
        result = negras['engine'].play(board, chess.engine.Limit(depth=negras['dados'].profundidade))
        board.push(result.move)
        node = node.add_variation(result.move)
    
    game.headers["Result"] = board.result()

    engineBrancas.quit()
    engineNegras.quit()
    return game

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

    #Para cada cenário, vamos realizar os pares de partidas entre os jogadores iniciados
    cenarios = session.query(Cenario).all()
    for cenario in cenarios:
        game1 = play_game(jogadorComRedesNeurais, jogadorSemRedesNeurais) 
        game2 = play_game(jogadorSemRedesNeurais, jogadorComRedesNeurais)

        # Save games to PGN
        nomeGame1 = jogadorComRedesNeurais.nome + ' vs ' + jogadorSemRedesNeurais.nome + '.pgn'
        nomeGame2 = jogadorSemRedesNeurais.nome + ' vs ' + jogadorComRedesNeurais.nome + '.pgn'
        with open(nomeGame1, "w") as f:
            f.write(str(game1))

        with open(nomeGame2, "w") as f:
            f.write(str(game2))

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
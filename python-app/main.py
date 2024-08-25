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

    informacoes_jogo = {
        "game": game,                                  # O objeto do jogo para gerar o pgn
        "lances": [move for move in board.move_stack], # Todos os lances realizados
        "resultado": game.headers["Result"],           # Resultado do jogo (1-0, 0-1, 1/2-1/2)
        "brancas_id": brancas['dados'].id,             # ID do jogador das Brancas
        "negras_id": negras['dados'].id,               # ID do jogador das Negras
        "cenario_id": cenario.id                       # ID do cenário do jogo
    }
    return jogo_info

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
        jogo1 = play_game(jogadorComRedesNeurais, jogadorSemRedesNeurais) 
        jogo2 = play_game(jogadorSemRedesNeurais, jogadorComRedesNeurais)

        # Save games to PGN
        nomeGame1 = jogadorComRedesNeurais.nome + ' vs ' + jogadorSemRedesNeurais.nome + '.pgn'
        nomeGame2 = jogadorSemRedesNeurais.nome + ' vs ' + jogadorComRedesNeurais.nome + '.pgn'
        with open(nomeGame1, "w") as f:
            f.write(str(jogo1['game']))

        with open(nomeGame2, "w") as f:
            f.write(str(jogo2['game']))
        
        partida1 = Partida()
        partida1.lances = ','.join(jogo1['lances'])
        partida1.resultado = jogo1['resultado']
        partida1.brancas_id = jogo1['brancas_id']
        partida1.negras_id = jogo1['negras_id']
        partida1.ambiente_id = 1
        partida1.cenario_id jogo1['cenario_id']

        partida2 = Partida()
        partida2.lances = ','.join(jogo2['lances'])
        partida2.resultado = jogo2['resultado']
        partida2.brancas_id = jogo2['brancas_id']
        partida2.negras_id = jogo2['negras_id']
        partida2.ambiente_id = 1
        partida2.cenario_id jogo2['cenario_id']

        session.add(partida1)
        session.add(partida2)

        session.commit()
    

if __name__ == "__main__":
    main(args.profundidadeEngineComRedesNeurais, args.profundidadeEngineSemRedesNeurais)
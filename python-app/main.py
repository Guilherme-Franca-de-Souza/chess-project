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

def registra_posicoes_partida(game):
    node = game
    while node:
        board = node.board()  # Recupera o tabuleiro atual
        pieces_info = informacoes_das_pecas(board)
        
        # Exibe ou processa as informações da posição
        print(f"Informações após o lance {node.move}:")
        for info in pieces_info:
            print(info)
        
        node = node.next()  # Avança para o próximo lance

def informacoes_das_pecas(board):
    # Iterar por todas as peças no tabuleiro
    pieces_info = []
    for square in chess.SQUARES:
        piece = board.piece_at(square)
        if piece:
            piece_info = {
                "tipo": piece.piece_type,
                "cor": "Branca" if piece.color == chess.WHITE else "Preta",
                "lances_legais": [],
                "lances_captura": [],
                "lances_promocao": [],
                "valor_ajustado": 0
            }

            # Obter os lances legais para essa peça
            for move in board.legal_moves:
                if move.from_square == square:
                    piece_info["lances_legais"].append(board.san(move))
                    if board.is_capture(move):
                        piece_info["lances_captura"].append(board.san(move))
                    if board.is_into_promotion(move):
                        piece_info["lances_promocao"].append(board.san(move))

            pieces_info.append(piece_info)


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

        registra_posicoes_partida(jogo1['game'])
        registra_posicoes_partida(jogo2['game'])

        session.commit()
    

if __name__ == "__main__":
    main(args.profundidadeEngineComRedesNeurais, args.profundidadeEngineSemRedesNeurais)
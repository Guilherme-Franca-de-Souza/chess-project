import chess
import chess.engine
import chess.pgn
import random
import os
from sqlalchemy import create_engine
from sqlalchemy import or_, and_, exists
from sqlalchemy.orm import sessionmaker
from models import Base, Posicao, Partida, Jogador, Avaliacao, Cenario, Ambiente
import time
import argparse

#captura argumentos
#parser = argparse.ArgumentParser(description='Recebe duas variáveis.')
#parser.add_argument('profundidadeEngineComRedesNeurais', type=str, help='Profundidade da engine com redes neurais')
#parser.add_argument('profundidadeEngineSemRedesNeurais', type=str, help='Profundidade da engine sem redes neurais')
#args = parser.parse_args()

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
    if (jogador_brancas.redes_neurais == 0):
        engineBrancas.configure({"Use NNUE": False})

    engineNegras = chess.engine.SimpleEngine.popen_uci(engine_path)
    if (jogador_negras.redes_neurais == 0):
        engineNegras.configure({"Use NNUE": False})

    brancas = {
        'engine': engineBrancas,
        'dados': jogador_brancas
    }

    negras = {
        'engine': engineNegras,
        'dados': jogador_negras
    }

    game = chess.pgn.Game()
    game.headers["White"] = brancas['dados'].nome
    game.headers["Black"] = negras['dados'].nome

    node = game

    print(fen)
    print(brancas['dados'].profundidade)
    print(negras['dados'].profundidade)
    while not board.is_game_over():
        result = brancas['engine'].play(board, chess.engine.Limit(depth=brancas['dados'].profundidade))
        #Garantir profundidade atingida:
        #print(result.info)
        board.push(result.move)
        node = node.add_variation(result.move)
        if board.is_game_over():
            break
        result = negras['engine'].play(board, chess.engine.Limit(depth=negras['dados'].profundidade))
        #Garantir profundidade atingida:
        #print(result.info)
        board.push(result.move)
        node = node.add_variation(result.move)

    game.headers["Result"] = board.result()

    engineBrancas.quit()
    engineNegras.quit()

    vencedor_id = None
    if game.headers["Result"] == "1-0":
        vencedor_id = brancas['dados'].id
    elif game.headers["Result"] == "0-1":
        vencedor_id = negras['dados'].id

    informacoes_jogo = {
        "game": game,                                  # O objeto do jogo para gerar o pgn
        "lances": [move.uci() for move in board.move_stack], # Todos os lances realizados
        "resultado": game.headers["Result"],           # Resultado do jogo (1-0, 0-1, 1/2-1/2)
        "brancas_id": brancas['dados'].id,             # ID do jogador das Brancas
        "negras_id": negras['dados'].id,               # ID do jogador das Negras
        "vencedor_id": vencedor_id,
        "cenario_id": cenario.id                       # ID do cenário do jogo
    }
    return informacoes_jogo

def calcular_material(board):
    valores_das_pecas = {
        chess.PAWN: 1,
        chess.KNIGHT: 3,
        chess.BISHOP: 3,
        chess.ROOK: 5,
        chess.QUEEN: 9,
        chess.KING: 0  # Rei não tem valor material em termos práticos
    }

    material_brancas = 0
    material_negras = 0

    for peca in valores_das_pecas:
        material_brancas += len(board.pieces(peca, chess.WHITE)) * valores_das_pecas[peca]
        material_negras += len(board.pieces(peca, chess.BLACK)) * valores_das_pecas[peca]

    return material_brancas - material_negras

def registra_posicoes_partida(game, partidaId, session):
    node = game
    sequencia = 1
    while node:
        board = node.board()  # Recupera o tabuleiro atual

        #informacoes_pecas = informacoes_das_pecas(board)

        posicao = Posicao()
        posicao.partida_id = partidaId
        posicao.fen = board.fen()
        posicao.numero_sequencia = sequencia
        posicao.diferenca_material = calcular_material(board)
        posicao.rei_brancas = []
        posicao.rei_negras = []
        posicao.dama_brancas = []
        posicao.dama_negras = []
        posicao.torres_brancas = []
        posicao.torres_negras = []
        posicao.cavalos_brancas = []
        posicao.cavalos_negras = []
        posicao.bispos_brancas = []
        posicao.bispos_negras = []
        posicao.peoes_brancas = []
        posicao.peoes_negras = []
        posicao.check = 1 if board.is_check() else 0
        posicao.mate = 1 if board.is_checkmate() else 0
        posicao.empate_material_insuficiente = 1 if board.is_insufficient_material() else 0
        posicao.empate_repeticoes = 1 if board.is_fivefold_repetition() else 0
        posicao.empate_50 = 1 if board.is_seventyfive_moves() else 0
        posicao.empate_afogamento = 1 if board.is_stalemate() else 0
        session.add(posicao)
        session.commit()

        node = node.next()  # Avança para o próximo lance
        sequencia+=1

def informacoes_das_pecas(board):
    pieces_info = []

    rei_brancas = []
    rei_negras = []
    dama_brancas = []
    dama_negras = []
    torres_brancas = []
    torres_negras = []
    cavalos_brancas = []
    cavalos_negras = []
    bispos_brancas = []
    bispos_negras = []
    peoes_brancas = []
    peoes_negras = []

    for square in chess.SQUARES:
        piece = board.piece_at(square)
        if piece:

            piece_info = {
                "tipo": piece.piece_type,
                "cor": "Branca" if piece.color == chess.WHITE else "Preta",
                "lances_legais": [],
                "lances_captura": [],
                "lances_promocao": [],
            }

            # Obter os lances legais para essa peça
            for move in board.legal_moves:
                if move.from_square == square:
                    san_move = board.san(move)
                    piece_info["lances_legais"].append(san_move)
                    if board.is_capture(move):
                        piece_info["lances_captura"].append(san_move)
                    if move.promotion:
                        piece_info["lances_promocao"].append(san_move)

            piece_type = piece.piece_type
            if piece_type == chess.PAWN:
                if piece.color == chess.WHITE:
                    peoes_brancas.append(piece_info)
                else:
                    peoes_negras.append(piece_info)
            elif piece_type == chess.KNIGHT:
                if piece.color == chess.WHITE:
                    cavalos_brancas.append(piece_info)
                else:
                    cavalos_negras.append(piece_info)
            elif piece_type == chess.BISHOP:
                if piece.color == chess.WHITE:
                    bispos_brancas.append(piece_info)
                else:
                    bispos_negras.append(piece_info)
            elif piece_type == chess.ROOK:
                if piece.color == chess.WHITE:
                    torres_brancas.append(piece_info)
                else:
                    torres_negras.append(piece_info)
            elif piece_type == chess.QUEEN:
                if piece.color == chess.WHITE:
                    dama_brancas.append(piece_info)
                else:
                    dama_negras.append(piece_info)
            elif piece_type == chess.KING:
                if piece.color == chess.WHITE:
                    rei_brancas.append(piece_info)
                else:
                    rei_negras.append(piece_info)

    pieces_info = {
        "rei_brancas": rei_brancas,
        "rei_negras": rei_negras,
        "dama_brancas": dama_brancas,
        "dama_negras": dama_negras,
        "torres_brancas": torres_brancas,
        "torres_negras": torres_negras,
        "cavalos_brancas": cavalos_brancas,
        "cavalos_negras": cavalos_negras,
        "bispos_brancas": bispos_brancas,
        "bispos_negras": bispos_negras,
        "peoes_brancas": peoes_brancas,
        "peoes_negras": peoes_negras
    }

    return pieces_info



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
        if (cenario.id < 3):
            partidaExistente = session.query(exists().where(
                    and_(
                        Partida.brancas_id == jogadorComRedesNeurais.id,
                        Partida.negras_id == jogadorSemRedesNeurais.id,
                        Partida.cenario_id == cenario.id
                    )
                )
            ).scalar()

            if (partidaExistente):
                print('JA EXISTE')
                continue
            jogo1 = play_game(jogadorComRedesNeurais, jogadorSemRedesNeurais, cenario)
            
            jogo2 = play_game(jogadorSemRedesNeurais, jogadorComRedesNeurais, cenario)

            lances1 = ','.join(jogo1['lances'])
            lances2 = ','.join(jogo2['lances'])

            lances1 = lances1[:2000]
            lances2 = lances2[:2000]

            partida1 = Partida()
            partida1.lances = lances1
            partida1.resultado = jogo1['resultado']
            partida1.brancas_id = jogo1['brancas_id']
            partida1.negras_id = jogo1['negras_id']
            partida1.vencedor_id = jogo1['vencedor_id']
            partida1.ambiente_id = 1
            partida1.cenario_id = cenario.id

            partida2 = Partida()
            partida2.lances = lances2
            partida2.resultado = jogo2['resultado']
            partida2.brancas_id = jogo2['brancas_id']
            partida2.negras_id = jogo2['negras_id']
            partida2.vencedor_id = jogo2['vencedor_id']
            partida2.ambiente_id = 1
            partida2.cenario_id = cenario.id

            session.add(partida1)
            session.add(partida2)
            session.commit()

            #registra_posicoes_partida(jogo1['game'], partida1.id, session)
            #registra_posicoes_partida(jogo2['game'], partida2.id, session)




if __name__ == "__main__":
    i = 0
    for com_redes_neurais in range(1, 26):
        for sem_redes_neurais in range(1, 26):
            i += 1
            start_time = time.time()
            main(com_redes_neurais, sem_redes_neurais)
            tempo = time.time() - start_time
            print(i, ' / ', tempo, ' ::: ', com_redes_neurais, ' / ', sem_redes_neurais)

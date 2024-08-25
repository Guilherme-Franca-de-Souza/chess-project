current_eval = info["score"].relative.score(mate_score=10000)

# Função para calcular o valor ajustado de uma peça removendo-a e avaliando o impacto
def get_adjusted_value(board, square):
    piece = board.remove_piece_at(square)
    
    # Avaliar a posição sem a peça
    info_without_piece = engine.analyse(board, chess.engine.Limit(depth=20))
    eval_without_piece = info_without_piece["score"].relative.score(mate_score=10000)
    
    # Recolocar a peça no tabuleiro
    board.set_piece_at(square, piece)
    
    # O valor ajustado é a diferença na avaliação
    if current_eval is not None and eval_without_piece is not None:
        return current_eval - eval_without_piece
    return 0  # Se a avaliação não for possível, retornamos 0

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

        # Obter o valor ajustado da peça
        piece_info["valor_ajustado"] = get_adjusted_value(board, square)

        # Obter os lances legais para essa peça
        for move in board.legal_moves:
            if move.from_square == square:
                piece_info["lances_legais"].append(board.san(move))
                if board.is_capture(move):
                    piece_info["lances_captura"].append(board.san(move))
                if board.is_into_promotion(move):
                    piece_info["lances_promocao"].append(board.san(move))

        pieces_info.append(piece_info)

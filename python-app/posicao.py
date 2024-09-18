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

# Aparentemente o stockfish guarda em cache avaliações de uma posição
# então se eu chamar essa função várias vezes para a mesma posição
# Ele vai sempre melhorar a análise
def get_best_lines(engine, board, depth=20, multipv=1):
    info = engine.analyse(board, chess.engine.Limit(depth=depth), multipv=multipv)
    return info

# Mostra as linhas de uma forma menos poluida
def get_line_str(line):
    line_str = ', '.join([move.uci() for move in line])
    return line_str
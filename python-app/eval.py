import subprocess
import re
import chess
import chess.engine


def eval(fen):
    engine = subprocess.Popen("/usr/games/stockfish", stdin=subprocess.PIPE,
                            stdout=subprocess.PIPE,
                            stderr=subprocess.STDOUT,
                            universal_newlines=True, bufsize=1)
                            #creationflags=subprocess.CREATE_NO_WINDOW)

    engine.stdin.write('uci\n')
    for eline in iter(engine.stdout.readline, ''):
        line = eline.strip()
        if 'uciok' in line:
            break

    engine.stdin.write('isready\n')
    for eline in iter(engine.stdout.readline, ''):
        line = eline.strip()
        if 'readyok' in line:
            break

    engine.stdin.write(f'position fen {fen}\n')
    engine.stdin.write('eval\n')

    evaluation = ["Não foi possível"]
    for eline in iter(engine.stdout.readline, ''):
        line = eline.strip()
        match = re.findall(r"Final evaluation\s+[-+]?\d*\.?\d+", line)
        if match:
            evaluation = re.findall(r"[-+]?\d*\.?\d+", match[0])
            break

    engine.stdin.write('quit\n')
    return evaluation[0]



fen = '8/3K3B/4p2P/2p1k1p1/8/p7/8/8 w - - 0 1'
print(eval(fen))

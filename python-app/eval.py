import subprocess

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

    for eline in iter(engine.stdout.readline, ''):
        line = eline.strip()
        print(line)
      
    engine.stdin.write('quit\n')

def main():
    fen = '8/3K3B/4p2P/2p1k1p1/8/p7/8/8 w - - 0 30'
    eval(fen)

if __name__ == '__main__':
    main()
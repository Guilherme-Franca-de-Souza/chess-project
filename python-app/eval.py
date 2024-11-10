import subprocess
import re
import chess
import chess.engine


def eval(fen):
    engine = subprocess.Popen("/usr/local/bin/stockfish", stdin=subprocess.PIPE,
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
    i = 0
    for eline in iter(engine.stdout.readline, ''):
        #print(i)
        line = eline.strip()
        print(line)
        #finalEvaluation = re.findall(r"Final evaluation:", line)
        #if (finalEvaluation):
        #    break
        #match = re.findall(r"Final evaluation\s+[-+]?\d*\.?\d+", line)
        #if match:
        #    evaluation = re.findall(r"[-+]?\d*\.?\d+", match[0])
        #    break

    engine.stdin.write('quit\n')
    #return evaluation[0]



fen = 'rnbqkbnr/1ppp1ppp/4p3/p3N3/3PPB2/N6B/PP1QPPPP/R3K2R b KQkq - 0 1'
print(eval(fen))

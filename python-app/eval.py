import subprocess
import re
import chess
import chess.engine


def eval(fen):
    engine = subprocess.Popen("/usr/local/bin/sf17/stockfish", stdin=subprocess.PIPE,
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
        #print(line)
        finalEvaluation = re.findall(r"Final evaluation:", line)
        if (finalEvaluation):
            break
        match = re.findall(r"Final evaluation\s+[-+]?\d*\.?\d+", line)
        if match:
            evaluation = re.findall(r"[-+]?\d*\.?\d+", match[0])
            break

    engine.stdin.write('quit\n')
    return evaluation[0]

#rkbqnbnr/1ppp1ppp/8/p5N1/3N4/3P1BBR/PP1QPPPP/R3K3 b Q - 0 1

fen = 'rbnqk1nr/1ppppbpp/8/1B4B1/p2NP3/2R1N3/1P4PP/3Q1RK1 b - - 0 1'
print(eval(fen))

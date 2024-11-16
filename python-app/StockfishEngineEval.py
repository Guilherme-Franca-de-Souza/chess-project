import subprocess
import re

class StockfishEngineEval:
    def __init__(self):
        self.engine = subprocess.Popen("/usr/local/bin/sf16/stockfish", stdin=subprocess.PIPE,
                                       stdout=subprocess.PIPE,
                                       stderr=subprocess.STDOUT,
                                       universal_newlines=True, bufsize=1)
        self._start_engine()

    def _start_engine(self):
        # Enviar comandos iniciais UCI
        self.engine.stdin.write('uci\n')
        for eline in iter(self.engine.stdout.readline, ''):
            line = eline.strip()
            if 'uciok' in line:
                break

        self.engine.stdin.write('isready\n')
        for eline in iter(self.engine.stdout.readline, ''):
            line = eline.strip()
            if 'readyok' in line:
                break

    def eval(self, fen):
        # Avaliar a posição com base no FEN fornecido
        self.engine.stdin.write(f'position fen {fen}\n')
        self.engine.stdin.write('eval\n')

        evaluation = ["N/A"]
        for eline in iter(self.engine.stdout.readline, ''):
            line = eline.strip()
            finalEvaluation = re.findall(r"Final evaluation:", line)
            match = re.findall(r"Final evaluation\s+[-+]?\d*\.?\d+", line)
            if match:
                evaluation = re.findall(r"[-+]?\d*\.?\d+", match[0])
                break
            if finalEvaluation:
                break

        return evaluation[0]

    def close(self):
        # Encerra o motor Stockfish
        self.engine.stdin.write('quit\n')
        self.engine.terminate()


# Criar uma instância global do motor Stockfish
stockfish = StockfishEngineEval()

# Função de avaliação que usa a instância global
def eval(fen):
    return stockfish.eval(fen)

# Certifique-se de encerrar o motor quando o script terminar
import atexit
atexit.register(stockfish.close)
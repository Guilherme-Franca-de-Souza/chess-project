import subprocess
import re

def eval(fen):
    # Inicia o subprocesso com Stockfish
    engine = subprocess.Popen(
        ["/usr/local/bin/stockfish"],
        stdin=subprocess.PIPE,
        stdout=subprocess.PIPE,
        stderr=subprocess.STDOUT,
        universal_newlines=True,
        bufsize=1
    )

    # Comandos UCI para configurar o Stockfish
    commands = [
        'uci\n',
        'setoption name EvalFile value ""\n',
        'isready\n',
        f'position fen {fen}\n',
        'eval\n',
        'quit\n'
    ]

    # Envia todos os comandos de uma vez usando communicate()
    output, _ = engine.communicate("".join(commands))

    # Processa a saída para encontrar a avaliação final
    evaluation = "Não foi possível"
    for line in output.splitlines():
        print(line)  # imprime cada linha para depuração
        match = re.search(r"Final evaluation\s+([-+]?\d*\.?\d+)", line)
        if match:
            evaluation = match.group(1)
            break

    return evaluation

# Teste com a FEN
fen = 'rbnqk1nr/1ppppbpp/8/1B4B1/p2NP3/2R1N3/1P4PP/3Q1RK1 b - - 0 1'
print(eval(fen))
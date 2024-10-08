import time
import random
import concurrent.futures
import random
import chess
import chess.engine
import StaticEvaluatorRN
from functools import lru_cache

def generate_random_value():
    """Gera um valor aleatório para um nó."""
    global count
    count += 1
    print(count)
    board = chess.Board()
    avaliacao = evaluator.evaluate(board)
    #return avaliacao
    return random.randint(-100, 100)

def negamax(node, depth, alpha, beta):
    """Implementa o algoritmo Negamax com poda alpha-beta."""
    if depth == 0:
        return generate_random_value()
    
    max_value = float('-inf')
    
    board = chess.Board()
    legal_moves = list(board.legal_moves)
    # Simula a geração de 60 nós filhos
    for _ in range(60):
        # Chamada recursiva para o próximo nível
        value = -negamax(node + 1, depth - 1, -beta, -alpha)
        
        max_value = max(max_value, value)
        alpha = max(alpha, value)
        
        if alpha >= beta:
            break  # Poda
    
    return max_value

def parallel_negamax(node, depth):
    """Executa a busca em paralelo para os nós filhos."""
    max_value = float('-inf')
    alpha = float('-inf')
    beta = float('inf')

    # Usando ThreadPoolExecutor para paralelismo
    with concurrent.futures.ThreadPoolExecutor() as executor:
        futures = [executor.submit(negamax, node + 1, depth - 1, -beta, -alpha) for _ in range(60)]
        
        for future in concurrent.futures.as_completed(futures):
            value = -future.result()
            max_value = max(max_value, value)
            alpha = max(alpha, value)
            if alpha >= beta:
                break  # Poda

    return max_value

if __name__ == "__main__":
    start_time = time.perf_counter()
    global evaluator
    global count
    count = 0
    engine = chess.engine.SimpleEngine.popen_uci("/usr/games/stockfish")
    evaluator = StaticEvaluatorRN.StaticEvaluatorRN()
    end_time = time.perf_counter()
    execution_time = end_time - start_time
    print(f"Tempo para iniciar: {execution_time:.2f} segundos")

    start_time = time.perf_counter()
    board = chess.Board()
    print(evaluator.evaluate(board))
    end_time = time.perf_counter()
    execution_time = end_time - start_time
    print(f"Tempo para executar a avaliação: {execution_time:.2f} segundos")

    start_time = time.perf_counter()
    depth = 3
    initial_node = 0
    best_value = parallel_negamax(initial_node, depth)
    print(f"Melhor valor encontrado: {best_value}")
    end_time = time.perf_counter()
    execution_time = end_time - start_time
    engine.quit()
    print(count)
    print(f"Tempo de execução: {execution_time:.2f} segundos")

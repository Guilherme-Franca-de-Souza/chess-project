import chess
import chess.engine
import random
import mysql.connector
from mysql.connector import Error
import os

# Configuração do Stockfish
engine = chess.engine.SimpleEngine.popen_uci("/usr/games/stockfish")

# Conexão com o MySQL
def create_connection():
    connection = None
    try:
        connection = mysql.connector.connect(
            host=os.getenv("DB_HOST", "localhost"),
            user=os.getenv("DB_USER", "root"),
            password=os.getenv("DB_PASSWORD", "password"),
            database=os.getenv("DB_NAME", "chess")
        )
        if connection.is_connected():
            print("Connected to MySQL database")
    except Error as e:
        print(f"The error '{e}' occurred")
    return connection

def create_tables(connection):
    cursor = connection.cursor()
    cursor.execute("""
    CREATE TABLE IF NOT EXISTS posicoes_iniciais (
        id INT AUTO_INCREMENT PRIMARY KEY,
        fen VARCHAR(255) NOT NULL,
        avaliacao FLOAT NOT NULL
    )""")
    cursor.execute("""
    CREATE TABLE IF NOT EXISTS sequencia (
        id INT AUTO_INCREMENT PRIMARY KEY,
        id_posicao_inicial INT,
        fen VARCHAR(255) NOT NULL,
        avaliacao FLOAT NOT NULL,
        FOREIGN KEY (id_posicao_inicial) REFERENCES posicoes_iniciais(id)
    )""")
    connection.commit()

def insert_initial_position(connection, fen, evaluation):
    cursor = connection.cursor()
    cursor.execute("""
    INSERT INTO posicoes_iniciais (fen, avaliacao) VALUES (%s, %s)
    """, (fen, evaluation))
    connection.commit()
    return cursor.lastrowid

def insert_sequence_position(connection, id_posicao_inicial, fen, evaluation):
    cursor = connection.cursor()
    cursor.execute("""
    INSERT INTO sequencia (id_posicao_inicial, fen, avaliacao) VALUES (%s, %s, %s)
    """, (id_posicao_inicial, fen, evaluation))
    connection.commit()

def get_random_fen():
    board = chess.Board()
    for _ in range(random.randint(1, 20)):
        move = random.choice(list(board.legal_moves))
        board.push(move)
    return board.fen()

def evaluate_position(fen):
    board = chess.Board(fen)
    result = engine.analyse(board, chess.engine.Limit(time=0.1))
    return result['score'].relative.score()

def main():
    connection = create_connection()
    create_tables(connection)

    random_fen = get_random_fen()
    initial_evaluation = evaluate_position(random_fen)
    print(initial_evaluation)
    #initial_id = insert_initial_position(connection, random_fen, initial_evaluation)

    #board = chess.Board(random_fen)
    #for move in board.legal_moves:
    #    board.push(move)
    #    fen = board.fen()
    #    evaluation = evaluate_position(fen)
    #    insert_sequence_position(connection, initial_id, fen, evaluation)
    #    board.pop()

if __name__ == "__main__":
    main()
    engine.quit()

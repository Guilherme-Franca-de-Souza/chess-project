from flask import Flask, jsonify
from flask_cors import CORS
import mysql.connector
import os

app = Flask(__name__)
CORS(app)  # Habilita CORS para todas as rotas

# Função para conectar ao banco de dados
def get_db_connection():
    return mysql.connector.connect(
        host="db",
        user="root",
        password="password",
        database="chess"
    )

@app.route('/hello', methods=['GET'])
def hello():
    return jsonify({"message": "ola"})

@app.route('/data', methods=['GET'])
def get_data():
    connection = get_db_connection()
    cursor = connection.cursor(dictionary=True)

    # Consulta para jogadores
    cursor.execute("SELECT id, redes_neurais FROM jogadores")
    players = cursor.fetchall()

    # Consulta para partidas
    cursor.execute("SELECT brancas_id, negras_id, vencedor_id FROM partidas")
    matches = cursor.fetchall()

    cursor.close()
    connection.close()

    return jsonify({'engines': players, 'matches': matches})

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=8888)

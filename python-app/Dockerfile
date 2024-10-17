# Dockerfile for Python App
FROM python:3.11

# Instalar dependências do sistema
RUN apt-get update && apt-get install -y --no-install-recommends \
    build-essential \
    stockfish \
    && rm -rf /var/lib/apt/lists/*

 
# Copy Stockfish 11 binaries into the container
COPY ./stockfish-11/ /usr/local/bin/stockfish-11/

# Ensure the binaries are executable
RUN chmod +x /usr/local/bin/stockfish-11/stockfish_20011801_x64* 

# Set environment variables if needed
ENV PATH="/usr/local/bin/stockfish-11:$PATH"

# Definir diretório de trabalho
WORKDIR /app

COPY . /app

# Copiar arquivo de dependências e instalar dependências do Python
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# Copiar código da aplicação
COPY . .

# Copiar o diretório de migrações do Alembic
COPY alembic alembic
COPY alembic.ini alembic.ini

EXPOSE 8888

CMD ["tail", "-f", "/dev/null"]
# Definir o comando padrão a ser executado quando o container é iniciado
#ENTRYPOINT ["jupyter", "notebook", "--ip=0.0.0.0", "--port=8888", "--no-browser", "--allow-root"]

# Dockerfile for Python App
#FROM python:3.11

# Instalar dependências do sistema
#RUN apt-get update && apt-get install -y --no-install-recommends \
#    build-essential \
#    stockfish \
#    && rm -rf /var/lib/apt/lists/*

# Dockerfile for Python App
FROM python:3.11

# Instalar dependências do sistema
RUN apt-get update && apt-get install -y --no-install-recommends \
    build-essential \
    stockfish \
    wget \
    && rm -rf /var/lib/apt/lists/*

# Baixar Stockfish 17 e extrair
RUN wget https://github.com/official-stockfish/Stockfish/archive/refs/tags/sf_17.zip -O stockfish.zip && \
    unzip stockfish.zip && \
    cd Stockfish-sf_17/src && \
    make build ARCH=x86-64-modern && \
    mkdir -p /usr/local/bin/sf17 && \
    mv ./stockfish /usr/local/bin/sf17/ && \
    cd ../.. && rm -rf Stockfish-sf_17 stockfish.zip

# Baixar Stockfish 16 e extrair
RUN wget https://github.com/official-stockfish/Stockfish/archive/refs/tags/sf_16.zip -O stockfish.zip && \
    unzip stockfish.zip && \
    cd Stockfish-sf_16/src && \
    make build ARCH=x86-64-modern && \
    mkdir -p /usr/local/bin/sf16 && \
    mv ./stockfish /usr/local/bin/sf16/ && \
    cd ../.. && rm -rf Stockfish-sf_16 stockfish.zip

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
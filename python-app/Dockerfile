# Dockerfile for Python App
FROM python:latest

# Instalar dependências do sistema
RUN apt-get update && apt-get install -y --no-install-recommends \
    build-essential \
    stockfish \
    && rm -rf /var/lib/apt/lists/*

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

# Definir o comando padrão a ser executado quando o container é iniciado
#ENTRYPOINT ["CMD", "sleep infinity"]
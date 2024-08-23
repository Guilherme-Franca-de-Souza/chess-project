from sqlalchemy import create_engine, Column, Integer, String, Float, ForeignKey, JSON, UniqueConstraint
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import relationship

Base = declarative_base()


class Posicao(Base):
    __tablename__ = 'posicoes'
    id = Column(Integer, primary_key=True, autoincrement=True)
    numero_sequencia = Column(Integer, nullable=False)
    fen = Column(String(4096), nullable=False)
    rei_brancas = Column(JSON, nullable=False)
    rei_negras = Column(JSON, nullable=False)
    dama_brancas = Column(JSON, nullable=False)
    dama_negras = Column(JSON, nullable=False)
    torres_brancas = Column(JSON, nullable=False)
    torres_negras = Column(JSON, nullable=False)
    bispos_brancas = Column(JSON, nullable=False)
    bispos_negras = Column(JSON, nullable=False)
    peoes_brancas = Column(JSON, nullable=False)
    peoes_negras = Column(JSON, nullable=False)
    check = Column(Integer, nullable=False, default=0)
    mate = Column(Integer, nullable=False, default=0)
    empate_repeticoes = Column(Integer, nullable=False, default=0)
    empate_50 = Column(Integer, nullable=False, default=0)
    empate_afogamento = Column(Integer, nullable=False, default=0)
    partida_id = Column(Integer, ForeignKey('partidas.id'), nullable=False)
    #RELACIONAMENTOS
    partida = relationship("Partida", back_populates="posicoes")

class Partida(Base):
    __tablename__ = 'partidas'
    id = Column(Integer, primary_key=True, autoincrement=True)
    lances = Column(String(2048), nullable=False)
    fen_inicial = Column(String(2048), nullable=False)
    descricao = Column(String(2048), nullable=False)
    resultado = Column(String(45), nullable=False)
    brancas_id = Column(Integer, ForeignKey('jogadores.id'), nullable=False)
    negras_id = Column(Integer, ForeignKey('jogadores.id'), nullable=False)
    ambiente_id = Column(Integer, ForeignKey('ambientes.id'), nullable=False)
    cenario_id = Column(Integer, ForeignKey('cenarios.id'), nullable=False)
    #RELACIONAMENTOS
    brancas = relationship("Jogador", foreign_keys=[brancas_id], back_populates="partidas")
    negras = relationship("Jogador", foreign_keys=[negras_id], back_populates="partidas")
    ambiente = relationship("Ambiente", back_populates="partidas")
    posicoes = relationship("Posicao", back_populates="partida")
    cenarios = relationship("Cenario", back_populates="partidas")
    #REGRAS
    __table_args__ = (UniqueConstraint('brancas_id', 'negras_id', 'fen_inicial', name='_brancas_negras_fen_inicial_uc'),)

class Jogador(Base):
    __tablename__ = 'jogadores'
    id = Column(Integer, primary_key=True, autoincrement=True)
    nome = Column(String(255), nullable=False)
    profundidade = Column(Integer, nullable=False)
    redes_neurais = Column(Integer, nullable=False)
    #RELACIONAMENTOS
    partidas_brancas = relationship("Partida", foreign_keys="[Partida.brancas_id]", back_populates="brancas")
    partidas_negras = relationship("Partida", foreign_keys="[Partida.negras_id]", back_populates="negras")

class Ambiente(Base):
    __tablename__ = 'ambientes'
    id = Column(Integer, primary_key=True, autoincrement=True)
    descricao = Column(String(4096), nullable=False)
    #RELACIONAMENTOS
    partidas = relationship("Partida", back_populates="ambiente")

class Avaliacao(Base):
    __tablename__ = 'avaliacoes'
    id = Column(Integer, primary_key=True, autoincrement=True)
    valor = Column(Float, nullable=False)
    tempo_segundos = Column(String(255), nullable=True)
    melhor_lance = Column(String(255), nullable=False)
    ambiente_id = Column(Integer, ForeignKey('ambientes.id'), nullable=False)
    jogador_id = Column(Integer, ForeignKey('jogadores.id'), nullable=False)
    posicao_id = Column(Integer, ForeignKey('posicoes.id'), nullable=False)
    #RELACIONAMENTOS
    ambiente = relationship("Ambiente", back_populates="avaliacoes")
    jogador = relationship("Jogador", back_populates="avaliacoes")
    posicao = relationship("Posicao", back_populates="avaliacoes")

class Cenario(Base):
    __tablename__ = 'cenarios'
    id = Column(Integer, primary_key=True, autoincrement=True)
    fen = Column(String(2048), nullable=False)
    descricao = Column(String(2048), nullable=False)
    #RELACIONAMENTOS
    partidas = relationship("Partida", back_populates="Cenario")
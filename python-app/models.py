from sqlalchemy import create_engine, Column, Integer, String, Float, ForeignKey
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import relationship

Base = declarative_base()

class PosicaoInicial(Base):
    __tablename__ = 'posicoes_iniciais'
    id = Column(Integer, primary_key=True, autoincrement=True)
    fen = Column(String(255), nullable=False)
    avaliacao = Column(Float, nullable=False)
    sequencias = relationship("Sequencia", back_populates="posicao_inicial")

class Sequencia(Base):
    __tablename__ = 'sequencia'
    id = Column(Integer, primary_key=True, autoincrement=True)
    id_posicao_inicial = Column(Integer, ForeignKey('posicoes_iniciais.id'))
    fen = Column(String(255), nullable=False)
    avaliacao = Column(Float, nullable=False)
    posicao_inicial = relationship("PosicaoInicial", back_populates="sequencias")

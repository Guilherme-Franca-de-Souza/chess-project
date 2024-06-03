from sqlalchemy import create_engine, Column, Integer, String, Float, ForeignKey
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import relationship

Base = declarative_base()

class Posicao(Base):
    __tablename__ = 'posicoes'
    id = Column(Integer, primary_key=True, autoincrement=True)
    fen = Column(String(255), nullable=False)
    avaliacao = Column(Float, nullable=False)
    qwp = Column(Integer, nullable=False)
    qbp = Column(Integer, nullable=False)
    qwr = Column(Integer, nullable=False)
    qbr = Column(Integer, nullable=False)
    qwn = Column(Integer, nullable=False)
    qbn = Column(Integer, nullable=False)
    qwb = Column(Integer, nullable=False)
    qbb = Column(Integer, nullable=False)
    qbq = Column(Integer, nullable=False)
    qbq = Column(Integer, nullable=False)
    sequencias = relationship("Sequencia", back_populates="posicoes")

class Sequencia(Base):
    __tablename__ = 'sequencias'
    id = Column(Integer, primary_key=True, autoincrement=True)
    id_posicao = Column(Integer, ForeignKey('posicoes.id'))
    ordem = Column(Integer, nullable=False)
    fen = Column(String(255), nullable=False)
    avaliacao = Column(Float, nullable=False)
    mate = Column(Integer, nullable=False, default=0)
    posicao = relationship("Posicao", back_populates="sequencias")

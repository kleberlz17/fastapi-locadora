from sqlalchemy import Column, Integer, Boolean, Date, ForeignKey
from sqlalchemy.orm import relationship
from app.database import Base

class Locacao(Base):
    __tablename__ = "locacao"

    id_locacao = Column(Integer, primary_key=True)
    id_cliente = Column(Integer, ForeignKey("cliente.id"), nullable=False)
    id_filme = Column(Integer, ForeignKey("filmes.id_filme"), nullable=False)

    data_locacao = Column(Date, nullable=False)
    data_devolucao = Column(Date, nullable=False)
    devolvido = Column(Boolean, nullable=False, default=False)
    quantidade = Column(Integer, nullable=False)

    ##Relacionamentos many to one
    cliente = relationship("Cliente", back_populates="locacoes")
    filme = relationship("Filmes", back_populates="locacoes")
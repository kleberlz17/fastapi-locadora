from sqlalchemy import Column, Integer, String, Date
from sqlalchemy.orm import relationship
from app.database import Base

class Filmes(Base):
    __tablename__ = "filmes"

    id_filme = Column(Integer, primary_key=True)
    nome = Column(String, nullable=False)
    data_lancamento = Column(Date, nullable=False)
    diretor = Column(String, nullable=False)
    genero = Column(String, nullable=False)
    estoque = Column(Integer, nullable=False)

    # Relação one to many
    locacoes = relationship("Locacao", back_populates="filme")
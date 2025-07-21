from app.database import Base, engine
from app.models.cliente import Cliente
from app.models.filmes import Filmes
from app.models.locacao import Locacao


##NECESSÁRIO PARA CRIAR AS TABELAS DENTRO DO  BANCO DE DADOS(POSTGRESQL)
Base.metadata.create_all(bind=engine)
print("Tabelas criadas com sucesso.")
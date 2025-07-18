from datetime import date
from os.path import exists

from fastapi import HTTPException
from app.repositories import filmes_repository
from app.models.filmes import Filmes
from sqlalchemy.orm import Session

class FilmeValidator:
    def __init__(self, db: Session):
        self.db = db

    def validar_estoque(self, estoque: int):
        if estoque <=0:
            raise HTTPException(status_code=400, detail="O estoque não deve ser negativo, somente 0 pra cima é permitido.")


    def validar_data_lancamento(self, data_lancamento: date):
        hoje = date.today()
        if (data_lancamento.year > hoje.year or
            (data_lancamento.year == hoje.year and data_lancamento.month > hoje.month)):
            raise HTTPException(status_code=400, detail="A data de lançamento digitada está num ponto futuro.")

    def validar_duplicidade_nome(self, nome: str, id_atual: int | None):
        existente = filmes_repository.get_by_nome_ignore_case(self.db, nome.strip()) # strip evita problemas com espaços em branco.
        if existente and existente.id_filme != id_atual:
            raise HTTPException(status_code=400, detail="Já existe um filme cadastrado com esse nome.")

    def validar_tudo(self, filme: Filmes):
        self.validar_duplicidade_nome(filme.nome, filme.id_filme)
        self.validar_estoque(filme.estoque)
        self.validar_data_lancamento(filme.data_lancamento)
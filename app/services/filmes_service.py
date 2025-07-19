from datetime import date
from typing import List

from fastapi import HTTPException
from sqlalchemy.orm import Session

from app.models.filmes import Filmes
from app.schemas.filmes_create import  FilmeCreate
from app.schemas.filmes_update import FilmeUpdate
from app.repositories.filmes_repository import (
get_by_id,
get_by_nome_ignore_case,
get_by_data_lancamento,
get_by_genero_contendo,
get_by_diretor_contendo,
get_by_estoque,
save,
delete,
)
from app.validators.filmes_validator import FilmeValidator

class FilmeService:
    def __init__(self, db:Session):
        self.db = db
        self.validator = FilmeValidator(db)

    def salvar(self, filme_create: FilmeCreate) -> Filmes:
        nome_ajustado = filme_create.nome.strip()
        if not nome_ajustado:
            raise HTTPException(status_code=400, detail="O nome do filme não pode ser vazio ou nulo.")

        filme = Filmes(**filme_create.dict())
        filme.nome = nome_ajustado

        self.validator.validar_tudo(filme)
        return save(self.db, filme)

    def buscar_por_id(self, id_filme: int) -> Filmes:
        filme = get_by_id(self.db, id_filme)
        if not filme:
            raise HTTPException(status_code=404, detail="Filme não encontrado.")
        return filme

    def buscar_por_nome(self, nome: str) -> List[Filmes]:
        return get_by_nome_ignore_case(self.db, nome)

    def buscar_por_data_lancamento(self, data: date) -> List[Filmes]:
        return get_by_data_lancamento(self.db, data)

    def buscar_por_diretor(self, diretor: str) -> List[Filmes]:
        return get_by_diretor_contendo(self.db, diretor)

    def buscar_por_genero(self, genero: str) -> List[Filmes]:
        return get_by_genero_contendo(self.db, genero)

    def buscar_por_estoque(self, estoque: int) -> List[Filmes]:
        return get_by_estoque(self.db, estoque)

    def alterar_estoque(self, id_filme: int, novo_estoque: int) -> Filmes:
        filme = self.buscar_por_id(id_filme)
        filme.estoque = novo_estoque
        self.validator.validar_estoque(novo_estoque)
        return save(self.db, filme)

    def alterar_data_lancamento(self, id_filme: int, nova_data: date) -> Filmes:
        if not nova_data:
            raise HTTPException(status_code=400, detail="A nova data não pode ser nula.")
        self.validator.validar_data_lancamento(nova_data)

        filme = self.buscar_por_id(id_filme)
        filme.data_lancamento = nova_data
        return save(self.db, filme)

    def alterar_nome(self, id_filme: int, novo_nome: str) -> Filmes:
        if not novo_nome.strip():
            raise HTTPException(status_code=400, detail="O nome não pode ser vazio.")
        self.validator.validar_duplicidade_nome(novo_nome, id_filme)

        filme = self.buscar_por_id(id_filme)
        filme.nome = novo_nome.strip() # Evita problema com espaços em branco
        return save(self.db, filme)

    def deletar(self, id_filme: int):
        filme = self.buscar_por_id(id_filme)
        delete(self.db, filme)
from datetime import date
from typing import List

from fastapi import HTTPException
from sqlalchemy.orm import Session

from app.models.filmes import Filmes
from app.utils.logger import logger
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
    delete, get_by_nome_contendo,
)
from app.validators.filmes_validator import FilmeValidator

class FilmeService:
    def __init__(self, db:Session):
        self.db = db
        self.validator = FilmeValidator(db)

    def salvar(self, filme_create: FilmeCreate) -> Filmes:
        nome_ajustado = filme_create.nome.strip()
        if not nome_ajustado:
            logger.warning("Tentativa de salvar filme com nome vazio.")
            raise HTTPException(status_code=400, detail="O nome do filme não pode ser vazio ou nulo.")

        logger.info(f"Salvando filme: {nome_ajustado}")
        filme = Filmes(**filme_create.dict())
        filme.nome = nome_ajustado

        self.validator.validar_tudo(filme)
        return save(self.db, filme)

    def buscar_por_id(self, id_filme: int) -> Filmes:
        logger.info(f"Buscando filme por ID: {id_filme}")
        filme = get_by_id(self.db, id_filme)
        if not filme:
            logger.warning(f"Filme com ID {id_filme} não encontrado.")
            raise HTTPException(status_code=404, detail="Filme não encontrado.")
        return filme

    def buscar_por_nome(self, nome: str) -> List[Filmes]:
        logger.info(f"Buscando filmes contendo no nome: {nome}")
        return get_by_nome_contendo(self.db, nome)

    def buscar_por_data_lancamento(self, data: date) -> List[Filmes]:
        logger.info(f"Buscando filmes por data de lançamento: {data}")
        return get_by_data_lancamento(self.db, data)

    def buscar_por_diretor(self, diretor: str) -> List[Filmes]:
        logger.info(f"Buscando filmes por diretor contendo: {diretor}")
        return get_by_diretor_contendo(self.db, diretor)

    def buscar_por_genero(self, genero: str) -> List[Filmes]:
        logger.info(f"Buscando filmes por gênero contendo: {genero}")
        return get_by_genero_contendo(self.db, genero)

    def buscar_por_estoque(self, estoque: int) -> List[Filmes]:
        logger.info(f"Buscando filmes com estoque igual a: {estoque}")
        return get_by_estoque(self.db, estoque)

    def alterar_estoque(self, id_filme: int, novo_estoque: int) -> Filmes:
        logger.info(f"Alterando estoque do filme ID {id_filme} para: {novo_estoque}")
        filme = self.buscar_por_id(id_filme)
        filme.estoque = novo_estoque
        self.validator.validar_estoque(novo_estoque)
        return save(self.db, filme)

    def alterar_data_lancamento(self, id_filme: int, nova_data: date) -> Filmes:
        if not nova_data:
            logger.warning("Tentativa de alterar data de lançamento com valor nulo.")
            raise HTTPException(status_code=400, detail="A nova data não pode ser nula.")

        logger.info(f"Alterando data de lançamento do filme ID {id_filme} para: {nova_data}")
        self.validator.validar_data_lancamento(nova_data)
        filme = self.buscar_por_id(id_filme)
        filme.data_lancamento = nova_data
        return save(self.db, filme)

    def alterar_nome(self, id_filme: int, novo_nome: str) -> Filmes:
        if not novo_nome.strip():
            logger.warning("Tentativa de alterar nome para valor vazio.")
            raise HTTPException(status_code=400, detail="O nome não pode ser vazio.")

        logger.info(f"Alterando nome do filme ID {id_filme} para: {novo_nome.strip()}")
        self.validator.validar_duplicidade_nome(novo_nome, id_filme)
        filme = self.buscar_por_id(id_filme)
        filme.nome = novo_nome.strip() # Evita problema com espaços em branco
        return save(self.db, filme)

    def deletar(self, id_filme: int):
        logger.info(f"Deletando filme ID: {id_filme}")
        filme = self.buscar_por_id(id_filme)
        delete(self.db, filme)
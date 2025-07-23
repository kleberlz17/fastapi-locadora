from datetime import date, datetime
from typing import List
from fastapi import HTTPException
from sqlalchemy.orm import Session

from app.models.locacao import Locacao
from app.models.cliente import Cliente
from app.models.filmes import Filmes
from app.schemas.locacao_create import LocacaoCreate
from app.schemas.locacao_update import LocacaoUpdate
from app.repositories import locacao_repository, cliente_repository, filmes_repository
from app.validators.locacao_validator import LocacaoValidator

class LocacaoService:
    def __init__(self, db: Session):
        self.db =db
        self.validator = LocacaoValidator(db)

    def salvar(self, locacao_create: LocacaoCreate) -> Locacao:
        print(f"id_cliente: {locacao_create.id_cliente}, id_filme: {locacao_create.id_filme}")
        cliente = cliente_repository.get_by_id(self.db, locacao_create.id_cliente)
        if not cliente:
            raise HTTPException(status_code=404, detail="Cliente não encontrado.")

        filme = filmes_repository.get_by_id(self.db, locacao_create.id_filme)
        print(f"Filme buscado: {filme}")
        if not filme:
            raise HTTPException(status_code=404, detail="Filme não encontrado.")

        locacao = Locacao(
            cliente = cliente,
            filme = filme,
            id_cliente = cliente.id, #Se não expor vai ficar comparando com NONE e a duplicidade vai passar.
            id_filme = filme.id_filme, #Se não expor vai ficar comparando com NONE e a duplicidade vai passar.
            data_locacao = locacao_create.data_locacao,
            data_devolucao = locacao_create.data_devolucao,
            devolvido = locacao_create.devolvido,
            quantidade = locacao_create.quantidade
        )

        self.validator.validar_tudo(locacao)
        filme.estoque -= locacao.quantidade
        filmes_repository.save(self.db, filme)

        return locacao_repository.save(self.db, locacao)

    def buscar_por_id(self, id_locacao: int) -> Locacao:
        locacao = locacao_repository.get_by_id(self.db, id_locacao)
        if not locacao:
            raise HTTPException(status_code=404, detail="Locação não encontrada.")
        return locacao

    def buscar_por_cliente_id(self, cliente_id: int) -> List[Locacao]:
        return locacao_repository.get_by_cliente_id(self.db, cliente_id)

    def buscar_por_filme_id(self, filme_id: int) -> List[Locacao]:
        return locacao_repository.get_by_filme_id(self.db, filme_id)

    def renovar_data_devolucao(self, id_locacao: int, nova_data: date) -> Locacao:
        if not nova_data:
            raise HTTPException(status_code=400, detail="A nova data de devolução não pode ser nula.")

        self.validator.validar_data_devolucao(nova_data)

        locacao = self.buscar_por_id(id_locacao)
        locacao.data_devolucao = nova_data
        return locacao_repository.save(self.db, locacao)

    def calcular_multa(self, id_locacao: int) -> float:
        locacao = self.buscar_por_id(id_locacao)

        if locacao.devolvido:
            return 0.0

        hoje = datetime.today().date()
        if locacao.data_devolucao >= hoje:
            return 0.0

        dias_atraso = (hoje - locacao.data_devolucao).days
        multa_por_dia = 7.00
        return dias_atraso * multa_por_dia

    def alugar_filme(self, id_cliente: int, id_filme: int, quantidade: int, data_devolucao: date) -> Locacao:
        cliente = cliente_repository.get_by_id(self.db, id_cliente)
        if not cliente:
            raise HTTPException(status_code=404, detail="Cliente não encontrado.")

        filme = filmes_repository.get_by_id(self.db, id_filme)
        if not filme:
            raise HTTPException(status_code=404, detail="Filme não encontrado.")

        if quantidade <= 0:
            raise HTTPException(status_code=400, detail="Estoque insuficiente.")

        locacao_temp = Locacao(
            cliente = cliente,
            filme = filme,
            id_cliente = cliente.id, #Se não expor vai ficar comparando com NONE e a duplicidade vai passar.
            id_filme = filme.id_filme, #Se não expor vai ficar comparando com NONE e a duplicidade vai passar.
            quantidade = quantidade,
            data_locacao = datetime.today().date(),
            data_devolucao = data_devolucao,
            devolvido = False
        )
        self.validator.validar_tudo(locacao_temp)

        filme.estoque -= quantidade
        filmes_repository.save(self.db, filme)

        return locacao_repository.save(self.db, locacao_temp)

    def deletar(self, id_locacao: int):
        locacao = self.buscar_por_id(id_locacao)
        locacao_repository.delete(self.db, locacao)
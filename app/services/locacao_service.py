from datetime import date, datetime
from typing import List
from fastapi import HTTPException
from sqlalchemy.orm import Session

from app.models.locacao import Locacao
from app.utils.logger import logger
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
        logger.info(f"Tentando salvar locação: cliente={locacao_create.id_cliente}, filme={locacao_create.id_filme}")

        cliente = cliente_repository.get_by_id(self.db, locacao_create.id_cliente)
        if not cliente:
            logger.warning(f"Cliente {locacao_create.id_cliente} não encontrado.")
            raise HTTPException(status_code=404, detail="Cliente não encontrado.")

        filme = filmes_repository.get_by_id(self.db, locacao_create.id_filme)
        if not filme:
            logger.warning(f"Filme {locacao_create.id_filme} não encontrado.")
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

        logger.info(f"Locação criada para cliente {cliente.id} do filme {filme.id_filme}")
        return locacao_repository.save(self.db, locacao)

    def buscar_por_id(self, id_locacao: int) -> Locacao:
        logger.info(f"Buscando locação por ID: {id_locacao}")
        locacao = locacao_repository.get_by_id(self.db, id_locacao)
        if not locacao:
            logger.warning(f"Locação {id_locacao} não encontrada.")
            raise HTTPException(status_code=404, detail="Locação não encontrada.")
        return locacao

    def buscar_por_cliente_id(self, cliente_id: int) -> List[Locacao]:
        logger.info(f"Buscando locações por cliente ID: {cliente_id}")
        locacao = locacao_repository.get_by_cliente_id(self.db, cliente_id)
        if not locacao:
            logger.warning(f"Cliente de ID {cliente_id} não possui locações.")
            raise HTTPException(status_code=404, detail="Locações não encontradas.")
        return locacao

    def buscar_por_filme_id(self, filme_id: int) -> List[Locacao]:
        logger.info(f"Buscando locações por filme ID: {filme_id}")
        locacao = locacao_repository.get_by_filme_id(self.db, filme_id)
        if not locacao:
            logger.warning(f"Filme de ID {filme_id} não possui locações.")
            raise HTTPException(status_code=404, detail ="Locações não encontradas.")
        return locacao

    def renovar_data_devolucao(self, id_locacao: int, nova_data: date) -> Locacao:
        if not nova_data:
            logger.warning("Tentativa de renovar data de devolução com valor nulo.")
            raise HTTPException(status_code=400, detail="A nova data de devolução não pode ser nula.")

        self.validator.validar_data_devolucao(nova_data)
        locacao = self.buscar_por_id(id_locacao)
        logger.info(f"Renovando data de devolução da locação {id_locacao} para {nova_data}")
        locacao.data_devolucao = nova_data
        return locacao_repository.save(self.db, locacao)

    def calcular_multa(self, id_locacao: int) -> float:
        logger.info(f"Calculando multa da locação {id_locacao}")
        locacao = self.buscar_por_id(id_locacao)

        if locacao.devolvido:
            logger.info(f"Locação {id_locacao} já devolvida. Multa = 0")
            return 0.0

        hoje = datetime.today().date()
        if locacao.data_devolucao >= hoje:
            logger.info(f"Locação {id_locacao} ainda dentro do prazo. Sem multa.")
            return 0.0

        dias_atraso = (hoje - locacao.data_devolucao).days
        multa_por_dia = 7.00
        logger.warning(f"Locação {id_locacao} em atraso ({dias_atraso} dias). Multa: R$ {multa_por_dia:.2f}")
        return dias_atraso * multa_por_dia

    def alugar_filme(self, id_cliente: int, id_filme: int, quantidade: int, data_devolucao: date) -> Locacao:
        logger.info(f"Processando aluguel: cliente={id_cliente}, filme={id_filme}, quantidade={quantidade}")
        cliente = cliente_repository.get_by_id(self.db, id_cliente)
        if not cliente:
            logger.warning(f"Cliente {id_cliente} não encontrado.")
            raise HTTPException(status_code=404, detail="Cliente não encontrado.")

        filme = filmes_repository.get_by_id(self.db, id_filme)
        if not filme:
            logger.warning(f"Filme {id_filme} não encontrado.")
            raise HTTPException(status_code=404, detail="Filme não encontrado.")

        if quantidade <= 0:
            logger.warning("Quantidade inválida para locação.")
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

        logger.info(f"Locação realizada: cliente={cliente.id}, filme={filme.id_filme}, quantidade={quantidade}")
        return locacao_repository.save(self.db, locacao_temp)

    def deletar(self, id_locacao: int):
        logger.info(f"Deletando locação ID: {id_locacao}")
        locacao = self.buscar_por_id(id_locacao)
        locacao_repository.delete(self.db, locacao)
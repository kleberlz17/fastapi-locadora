from datetime import date
from fastapi import HTTPException
from sqlalchemy.orm import Session
from app.models.locacao import Locacao
from app.models.filmes import Filmes

class LocacaoValidator:
    def __init__(self, db: Session):
        self.db = db


    def validar_data_locacao(self, data_locacao: date):
        if data_locacao > date.today():
            raise HTTPException(status_code=400, detail="A data de locação digitada está num ponto futuro.")

    def validar_data_devolucao(self, data_devolucao: date):
        if data_devolucao < date.today():
            raise HTTPException(status_code=400, detail= "A data de devolução digitada está num ponto passado.")

    def validar_quantidade(self, quantidade: int):
        if quantidade < 0:
            raise HTTPException(status_code=400, detail="A quantidade não deve ser negativa, somente de 0 pra cima é permitido.")

    def validar_duplicidade(self, locacao: Locacao):

        locacao_existente = self.db.query(Locacao).filter(
    Locacao.id_cliente == locacao.id_cliente,
            Locacao.id_filme == locacao.id_filme,
            Locacao.data_locacao == locacao.data_locacao,
            Locacao.devolvido == False
        ).first()

        if locacao_existente:
            raise HTTPException(status_code=400, detail="Já existe uma locação semelhante em aberto.")


    def validar_estoque(self, locacao: Locacao):
        filme = locacao.filme
        if not filme:
            raise HTTPException(
                status_code=404,
                detail="Filme não encontrado."
            )
        if filme.estoque < locacao.quantidade:
            raise HTTPException(
                status_code=400,
                detail="Estoque insuficiente para essa locação."
            )

    def validar_tudo(self, locacao: Locacao):
        self.validar_data_locacao(locacao.data_locacao)
        self.validar_data_devolucao(locacao.data_devolucao)
        self.validar_quantidade(locacao.quantidade)
        self.validar_duplicidade(locacao)
        self.validar_estoque(locacao)
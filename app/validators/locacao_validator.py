from datetime import date
from fastapi import HTTPException
from app.models.locacao import Locacao

class LocacaoValidator:
    def validar_data_locacao(self, data_locacao: date):
        if data_locacao > date.today():
            raise HTTPException(status_code=400, detail="A data de locação digitada está num ponto futuro.")

    def validar_data_devolucao(self, data_devolucao: date):
        if data_devolucao < date.today():
            raise HTTPException(status_code=400, detail= "A data de devolução digitada está num ponto passado.")

    def validar_quantidade(self, quantidade: int):
        if quantidade < 0:
            raise HTTPException(status_code=400, detail="A quantidade não deve ser negativa, somente de 0 pra cima é permitido.")

    def validar_tudo(self, locacao: Locacao):
        self.validar_data_locacao(locacao.data_locacao)
        self.validar_data_devolucao(locacao.data_devolucao)
        self.validar_quantidade(locacao.quantidade)
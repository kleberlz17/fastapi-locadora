from pydantic import BaseModel, Field
from datetime import date

class LocacaoResponse(BaseModel):
    ##UTILIZADO PARA RESPONDER (GET)
    id_locacao: int = Field(
        ..., #obrigatorio
        description="Identificador único da locação"
    )

    id_cliente: int = Field(
        ..., #obrigatorio
        description="ID do cliente"
    )

    id_filme: int = Field(
        ..., #obrigatorio
        description="ID do filme"
    )

    data_locacao: date = Field(
        ..., #obrigatorio
        description="Data de locação no formato AAAA-MM-DD"
    )

    data_devolucao: date = Field(
        ..., #obrigatorio
        description="Data de devolução no formato AAAA-MM-DD"
    )

    devolvido: bool = Field(
        ..., #obrigatorio
        description="Devolvido entre True ou False"
    )

    quantidade: int = Field(
        ..., #obrigatorio
        description="Quantas unidades foram alugadas"
    )

    class Config:
        orm_mode = True ##SEM ISSO O RETORNO DO SQLALCHEMY NAO FUNCIONA!!!!
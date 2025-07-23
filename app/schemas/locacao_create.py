from pydantic import BaseModel, Field
from datetime import date

class LocacaoCreate(BaseModel):
    ##UTILIZADO PARA CRIAR (POST)
    id_cliente: int = Field( ##ID DO CLIENTE
        ..., #obrigatoriedade
        ge=1,
        le=999999,
        description="ID do cliente"
    )

    id_filme: int = Field(
        ..., #obrigatoriedade
        ge=1,
        le=999999,
        description="ID do filme"
    )

    data_locacao: date = Field(
        ..., #obrigatoriedade
        description="Data de locação no formato AAAA-MM-DD"
    )

    data_devolucao: date = Field(
        ..., #obrigatoriedade
        description="Data de devolução no formato AAAA-MM-DD"
    )

    quantidade: int = Field(
        ..., #obrigatoriedade
        ge=1, #minimo 1 unidade
        description="Quantas unidades quer alugar"
    )

    devolvido: bool = Field(
        ..., #obrigatoriedade
        description="Devolvido entre True ou False"
    )
from pydantic import BaseModel, Field
from datetime import date
from typing import Optional

class LocacaoUpdate(BaseModel):
    # UTILIZADO PARA ATUALIZAR PARCIALMENTE(PATCH/PUT)
    id: Optional[int] = Field( #ID DO CLIENTE
        None,
        ge=1,
        le=999999,
        description="ID do cliente"
    )

    id_filme: Optional[int] = Field(
        ge=1,
        le=999999,
        description="ID do filme"
    )

    data_locacao: Optional[date] = Field(
        None,
        description="Data de locação no formato AAAA-MM-DD"
    )

    data_devolucao: Optional[date] = Field(
        None,
        description="Data de devolução no formato AAAA-MM-DD"
    )

    devolvido: Optional[bool] = Field(
        None,
        description="Devolvido entre True ou False"
    )

    quantidade: Optional[int] = Field(
        None,
        ge=1,
        description="Quantas unidades quer alugar"
    )

class RenovarLocacao(BaseModel):
    data_devolucao: date = Field(..., description="Nova data de devolução no formato AAAA-MM-DD")


class AluguelRequest(BaseModel):
    id_cliente: int = Field(..., ge=1, description="ID do cliente")
    id_filme: int = Field(..., ge=1, description="ID do filme")
    quantidade: int = Field(..., ge=1, description="Quantidade de unidades para alugar")
    data_devolucao: date = Field(..., description="Data prevista para devolução no formato AAAA-MM-DD")


class LocacaoOnlyId(BaseModel):
    id: int = Field(..., ge=1, description="ID da locação")
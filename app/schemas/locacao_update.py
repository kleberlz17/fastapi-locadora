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

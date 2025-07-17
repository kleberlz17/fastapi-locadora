from pydantic import BaseModel, Field
from datetime import date
from typing import Optional

class LocacaoDTO(BaseModel):
    id_locacao: Optional[int] = Field(
        default=None,
        ge=1,
        le=999999,
        description="Identificador único da locação"
    )

    id: int = Field( #Id do cliente
        ..., #3 pontinhos = obrigatório
        ge=1,
        le=999999,
        description="ID do cliente"
    )

    id_filmes: int = Field(
        ..., #3 pontinhos = obrigatório
        ge=1,
        le=999999,
        description="ID do filme"
    )

    data_locacao: date = Field(
        ..., #3 pontinhos = obrigatório
        description="Data de locação no formato AAAA-MM-DD"
    )

    data_devolucao: date = Field(
        ..., #3 pontinhos = obrigatório
        description="Data de devolução no formato AAAA-MM-DD"
    )

    devolvido: bool = Field(
        default=False, #Valor padrão é false.
        description="Devolvido entre true ou false"
    )

    quantidade: int = Field(
        ...,
        ge=1, #Minimo 1 unidade.
        description="Quantas unidades quer alugar"
    )
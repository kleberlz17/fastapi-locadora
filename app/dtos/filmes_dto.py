from pydantic import BaseModel, Field, constr
from datetime import date
from typing import Optional

class FilmeDTO(BaseModel):
    id_filme: Optional[int] = Field(
        default=None,
        ge=1,
        le=999999,
        description="Identificador único do filme"
    )

    nome: constr(min_length=1, max_length=100) = Field(
        ..., #3 pontinhos = obrigatório
        description="Nome completo do filme"
    )

    data_lancamento: date = Field(
        ..., #3 pontinhos = obrigatório
        description="Data de lançamento no formato AAAA-MM-DD"
    )

    diretor: constr(min_length=3, max_length=100) = Field(
        ..., #3 pontinhos = obrigatório
        description="Nome do diretor"
    )

    genero: constr(min_length=3, max_length=50) = Field(
        ...,
        description="Gênero do filme"
    )

    estoque: int = Field(
        ..., #3 pontinhos = obrigatório
        ge=0, #Garantir que não seja negativo
        description="Estoque do filme em número"
    )
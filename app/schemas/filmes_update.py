from pydantic import BaseModel, Field, constr
from datetime import date
from typing import Optional

class FilmeUpdate(BaseModel):
    # UTILIZADO PARA ATUALIZAR PARCIALMENTE(PATCH/PUT)
    nome: Optional[constr(min_length=1, max_length=100)] = Field(
        None,
        description="Nome completo do filme"
    )

    data_lancamento: Optional[date] = Field(
        None,
        description="Data de lançamento no formato AAAA-MM-DD"
    )

    diretor: Optional[constr(min_length=3, max_length=100)] = Field(
        None,
        description="Nome do diretor"
    )

    genero: Optional[constr(min_length=3, max_length=50)] = Field(
        None,
        description="Gênero do filme"
    )

    estoque: Optional[int] = Field(
        None,
        ge=0,
        description="Estoque do filme em número"
    )
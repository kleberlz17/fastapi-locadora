from pydantic import BaseModel, Field, constr
from datetime import date

class FilmeCreate(BaseModel):
    ##UTILIZADO PARA CRIAR (POST)
    nome: constr(min_length=1, max_length=100) = Field(
        ..., #3 pontos, obrigatoriedade
        description="Nome completo do filme"
    )

    data_lancamento: date = Field(
        ..., #3 pontos, obrigatoriedade
        description="Data de lançamento no formato AAAA-MM-DD"
    )

    diretor: constr(min_length=3, max_length=100) = Field(
        ..., #3 pontos, obrigatoriedade
        description="Nome do diretor"
    )

    genero: constr(min_length=3, max_length=50) = Field(
        ..., #3 pontos, obrigatoriedade
        description="Gênero do filme"
    )

    estoque: int = Field(
        ..., #3 pontos, obrigatoriedade
        ge=0,
        description="Estoque do filme em número"
    )
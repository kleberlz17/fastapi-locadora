from pydantic import BaseModel, Field, EmailStr, constr
from datetime import date
from typing import Optional

class ClienteDTO(BaseModel):
    id: Optional[int] = Field(
        default=None,
        ge=1,
        le=999999,
        description="Identificador único do cliente"
    )

    nome: constr(min_length=3, max_length=100) = Field(
        ..., #3 pontinhos = obrigatório
        description="Nome completo do cliente"
    )

    data_nascimento: date = Field(
        ..., #3 pontinhos = obrigatório
        description="Data de nascimento no formato AAAA-MM-DD"
    )

    cpf: constr(regex=r'^\d{11}$') = Field(
        ..., #3 pontinhos = obrigatório
        description="Número de telefone com DDD, apenas números"
    )

    email: EmailStr = Field( ##EmailStr já valida se o email é valido.
        ..., #3 pontinhos = obrigatório
        description="Endereço de e-mail válido"
    )

    endereco: constr(min_length=5, max_length=100) = Field(
        ..., #3 pontinhos = obrigatório
        description="Endereço residencial do cliente"
    )
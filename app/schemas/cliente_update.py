from pydantic import BaseModel, Field, EmailStr, constr
from datetime import date
from typing import Optional

class ClienteUpdate(BaseModel):
    #UTILIZADO PARA ATUALIZAR PARCIALMENTE(PATCH/PUT)
    nome: Optional[constr(min_length=3, max_length=100)] = Field(
        None,
        description="Nome completo do cliente"
    )

    data_nascimento: Optional[date] = Field(
        None,
        description="Data de nascimento no formato AAAA-MM-DD"
    )

    cpf: Optional[constr(regex=r'^\d{11}$')] = Field(
        None,
        description="CPF com 11 dígitos numéricos"
    )

    telefone: constr(min_length=8, max_length=15) = Field(
        ...,
        description="Número de telefone")

    email: Optional[EmailStr] = Field(
        None,
        description="Endereço de e-mail válido"
    )

    endereco: Optional[constr(min_length=5, max_length=100)] = Field(
        None,
        description="Endereço residencial do cliente"
    )

class NovoEmail(BaseModel):
    email: EmailStr = Field(..., description="Novo e-mail do cliente")


class NovoEndereco(BaseModel):
    endereco: constr(min_length=5, max_length=100) = Field(..., description="Novo endereço do cliente")


class NovoTelefone(BaseModel):
    telefone: constr(min_length=8, max_length=20) = Field(..., description="Novo telefone do cliente")


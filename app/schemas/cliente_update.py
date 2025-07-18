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

    email: Optional[EmailStr] = Field(
        None,
        description="Endereço de e-mail válido"
    )

    endereco: Optional[constr(min_length=5, max_length=100)] = Field(
        None,
        description="Endereço residencial do cliente"
    )

from pydantic import BaseModel, Field, EmailStr, constr
from datetime import date

class ClienteCreate(BaseModel):
    ##UTILIZADO PARA CRIAR (POST)
    nome: constr(min_length=3, max_length=100) = Field(
        ..., # 3 pontinhos = obrigatório.
        description="Nome completo do cliente"
    )

    data_nascimento: date = Field(
        ..., # 3 pontinhos = obrigatório.
        description="Data de nascimento no formato AAAA-MM-DD"
    )

    cpf: constr(regex=r'^\d{11}$') = Field(
        ..., # 3 pontinhos = obrigatório.
        description="CPF com 11 dígitos numéricos"
    )

    email: EmailStr = Field(
        ..., # 3 pontinhos = obrigatório.
        description="Endereço de e-mail válido"
    )

    endereco: constr(min_length=5, max_length=100) = Field(
        ..., # 3 pontinhos = obrigatório.
        description="Endereço residencial do cliente"
    )
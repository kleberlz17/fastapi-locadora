from pydantic import BaseModel, EmailStr, constr
from datetime import date

class ClienteResponse(BaseModel):
    ##UTILIZADO PARA RESPONDER (GET)
    id: int
    nome: constr(min_length=3, max_length=100)
    data_nascimento: date
    cpf: constr(regex=r'^\d{11}$')
    email = EmailStr
    endereco: constr(min_length=5, max_length=100)

    class Config:
        orm_mode = True # Permite retornar objects direto
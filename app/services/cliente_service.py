from fastapi import HTTPException, status
from sqlalchemy.orm import Session
from typing import List, Optional

from app.models.cliente import Cliente
from app.schemas.cliente_create import ClienteCreate
from app.schemas.cliente_update import ClienteUpdate
from app.schemas.cliente_response import ClienteResponse
from app.validators.cliente_validator import ClienteValidator
from app.repositories.cliente_repository import (
    get_by_id,
    get_by_telefone,
    get_by_email,
    get_by_cpf_ignore_case,
    get_by_nome_ignore_case,
)

class ClienteService:
    def __init__(self, db: Session):
        self.db = db
        self.validator = ClienteValidator(db)

    def salvar(self, cliente_create: ClienteCreate) -> ClienteResponse:
        if not cliente_create.cpf:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail="CPF é obrigatório"
            )

        cliente = Cliente(**cliente_create.dict())
        self.db.add(cliente)
        self.db.commit()
        self.db.refresh(cliente)
        return ClienteResponse.from_orm(cliente) #ClienteResponse define o formato da resposta, porém os dados vem da entidade Cliente.

    def buscar_por_id(self, id: int) -> ClienteResponse:
        cliente = get_by_id(self.db, id)
        if not cliente:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="Cliente não encontrado"
            )
        return ClienteResponse.from_orm(cliente) #ClienteResponse define o formato da resposta, porém os dados vem da entidade Cliente.

    def buscar_por_nome(self, nome: str) -> list[ClienteResponse]:
        clientes = get_by_nome_ignore_case(self.db, nome)
        return [ClienteResponse.from_orm(cliente) for cliente in clientes] #ClienteResponse define o formato da resposta, porém os dados vem da entidade Cliente.

    def buscar_por_cpf(self, cpf: str) -> ClienteResponse:
        cliente = get_by_cpf_ignore_case(self.db, cpf)
        if not cliente:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="Cliente não encontrado pelo CPF"
            )
        return ClienteResponse.from_orm(cliente) #ClienteResponse define o formato da resposta, porém os dados vem da entidade Cliente.

    def buscar_por_email(self, email: str) -> ClienteResponse:
        cliente = get_by_email(self.db, email)
        if not cliente:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="Cliente não encontrado pelo email"
            )
        return ClienteResponse.from_orm(cliente) #ClienteResponse define o formato da resposta, porém os dados vem da entidade Cliente.

    def buscar_por_telefone(self, telefone: str) -> ClienteResponse:
        cliente = get_by_telefone(self.db, telefone)
        if not cliente:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="Cliente não encontrado pelo telefone"
            )
        return ClienteResponse.from_orm(cliente) #ClienteResponse define o formato da resposta, porém os dados vem da entidade Cliente.

    def atualizar(self, id: int, cliente_update: ClienteUpdate) -> ClienteResponse:
        cliente = get_by_id(self.db, id)
        if not cliente:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="Cliente não encontrado"
            )

        for campo, valor in cliente_update.dict(exclude_unset=True).items():
            setattr(cliente, campo, valor)

        self.db.commit()
        self.db.refresh(cliente)
        return ClienteResponse.from_orm(cliente) #ClienteResponse define o formato da resposta, porém os dados vem da entidade Cliente.

    def alterar_telefone(self, id: int, telefone_novo: str) -> ClienteResponse:
        if not telefone_novo:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail="O novo telefone não deve ser nulo ou vazio."
            )

        cliente = get_by_id(self.db, id)
        if not cliente:
            raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Cliente não encontrado.")

        cliente.telefone = telefone_novo
        self.validator.validar_telefone(cliente)
        self.db.commit()
        self.db.refresh(cliente)
        return ClienteResponse.from_orm(cliente) #ClienteResponse define o formato da resposta, porém os dados vem da entidade Cliente.

    def alterar_email(self, id: int, email_novo: str) -> ClienteResponse:
        if not email_novo:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail="O novo email não deve ser nulo ou vazio."
            )

        cliente = get_by_id(self.db, id)
        if not cliente:
            raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Cliente não encontrado.")

        cliente.email = email_novo
        self.validator.validar_email(cliente)
        self.db.commit()
        self.db.refresh(cliente)
        return ClienteResponse.from_orm(cliente) #ClienteResponse define o formato da resposta, porém os dados vem da entidade Cliente.

    def alterar_endereco(self, id: int, endereco_novo: str) -> ClienteResponse:
        if not endereco_novo:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail="O novo endereço não deve ser nulo ou vazio."
            )

        cliente = get_by_id(self.db, id)
        if not cliente:
            raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Cliente não encontrado.")

        cliente.endereco = endereco_novo
        self.db.commit()
        self.db.refresh(cliente)
        return ClienteResponse.from_orm(cliente) #ClienteResponse define o formato da resposta, porém os dados vem da entidade Cliente.

    def deletar(self, id: int):
        cliente = get_by_id(self.db, id)
        if not cliente:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="Cliente não encontrado."
            )

        self.db.delete(cliente)
        self.db.commit()

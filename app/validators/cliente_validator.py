from fastapi import HTTPException
from app.repositories import cliente_repository
from app.models.cliente import Cliente

class ClienteValidator:
    def __init__(self, db):
        self.db = db

    def validar_cliente(self, cliente: Cliente):
        if self._cpf_ja_usado_por_outro(cliente):
            raise HTTPException(status_code=400, detail="CPF já cadsatrado, cliente existe no sistema.")


    def validar_email(self, cliente: Cliente):
        if self._email_ja_usado_por_outro(cliente):
            raise HTTPException(status_code=400, detail="Email já cadastrado, cliente existe no sistema.")


    def validar_telefone(self, cliente: Cliente):
        if self._telefone_ja_usado_por_outro(cliente):
            raise HTTPException(status_code=400, detail="Telefone já cadastrado, cliente existe no sistema.")


    def _cpf_ja_usado_por_outro(self, cliente: Cliente) -> bool:
        existente = cliente_repository.get_by_cpf_ignore_case(self.db, cliente.cpf)
        return existente is not None and existente.id != cliente.id

    def _email_ja_usado_por_outro(self, cliente: Cliente) -> bool:
        existente = cliente_repository.get_by_email(self.db, cliente.email)
        return existente is not None and existente.id != cliente.id

    def _telefone_ja_usado_por_outro(self, cliente: Cliente) -> bool:
        existente = cliente_repository.get_by_telefone(self.db, cliente.telefone)
        return existente is not None and existente.id != cliente.id
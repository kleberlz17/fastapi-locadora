from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
from typing import List

from app.database import get_db
from app.schemas.cliente_create import ClienteCreate
from app.schemas.cliente_response import ClienteResponse
from app.schemas.cliente_update import ClienteUpdate, NovoEmail, NovoEndereco, NovoTelefone
from app.services.cliente_service import ClienteService

router = APIRouter() #caminho está no init

@router.post("/salvar", status_code=status.HTTP_201_CREATED)
def salvar(cliente_create: ClienteCreate, db: Session = Depends(get_db)):
    service = ClienteService(db)
    cliente = service.salvar(cliente_create)
    return {"id": cliente.id}


@router.get("/{id}", response_model=ClienteResponse)
def buscar_por_id(id: int, db: Session = Depends(get_db)):
    service = ClienteService(db)
    return service.buscar_por_id(id)

@router.get("/nome/{nome}", response_model=List[ClienteResponse])
def buscar_por_nome(nome: str, db: Session = Depends(get_db)):
    service = ClienteService(db)
    clientes = service.buscar_por_nome(nome)
    if not clientes:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Nenhum cliente encontrado.")
    return clientes

@router.get("/cpf/{cpf}", response_model=ClienteResponse)
def buscar_por_cpf(cpf: str, db: Session = Depends(get_db)):
    service = ClienteService(db)
    return service.buscar_por_cpf(cpf)

@router.put("/{id}", response_model=ClienteResponse)
#Esse é genérico, atualiza qualquer conjunto de campos enviados, sem precisar de endpoint pra cada campo.
def atualizar_cliente(id: int, cliente_update: ClienteUpdate, db: Session = Depends(get_db)):
    service = ClienteService(db)
    return service.atualizar(id, cliente_update)

@router.put("/{id}/novoTelefone", response_model=ClienteResponse)
def alterar_telefone(id: int, novo_telefone: NovoTelefone, db: Session = Depends(get_db)):
    service = ClienteService(db)
    return service.alterar_telefone(id, novo_telefone.telefone)

@router.put("/{id}/novoEmail", response_model=ClienteResponse)
def alterar_email(id: int, novo_email: NovoEmail, db: Session = Depends(get_db)):
    service = ClienteService(db)
    return service.alterar_email(id, novo_email.email)

@router.put("/{id}/novoEndereco", response_model=ClienteResponse)
def alterar_endereco(id: int, novo_endereco: NovoEndereco, db: Session = Depends(get_db)):
    service = ClienteService(db)
    return service.alterar_endereco(id, novo_endereco.endereco)

@router.delete("/{id}/deletar", status_code=status.HTTP_204_NO_CONTENT)
def deletar_cliente(id: int, db: Session = Depends(get_db)):
    service = ClienteService(db)
    service.deletar(id)
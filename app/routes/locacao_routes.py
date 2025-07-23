from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
from typing import List

from app.repositories import filmes_repository
from app.database import get_db
from app.schemas.locacao_create import LocacaoCreate
from app.schemas.locacao_update import LocacaoUpdate, RenovarLocacao, AluguelRequest, LocacaoOnlyId
from app.schemas.locacao_response import LocacaoResponse
from app.services.locacao_service import LocacaoService

router = APIRouter()

@router.post("/salvar", status_code=status.HTTP_201_CREATED)
def salvar_locacao(locacao_create: LocacaoCreate, db: Session = Depends(get_db)):
    service = LocacaoService(db)
    locacao = service.salvar(locacao_create)
    return {"id": locacao.id_locacao}

@router.get("/{id}/locacoes", response_model=List[LocacaoResponse])
def buscar_por_cliente(id: int, db: Session = Depends(get_db)):
    service = LocacaoService(db)
    return service.buscar_por_cliente_id(id)

@router.get("/{idFilme}/historico", response_model=List[LocacaoResponse])
def buscar_historico_filme(idFilme: int, db: Session = Depends(get_db)):
    service = LocacaoService(db)
    return service.buscar_por_filme_id(idFilme)

@router.put("/{idLocacao}/renovarLocacao", response_model=LocacaoResponse)
def renovar_locacao(idLocacao: int, renovacao: RenovarLocacao, db: Session = Depends(get_db)):
    service = LocacaoService(db)
    return service.renovar_data_devolucao(idLocacao, renovacao.data_devolucao)

@router.post("/{idLocacao}/multa", response_model=float)
def calcular_multar(idLocacao: int, db: Session = Depends(get_db)):
    service = LocacaoService(db)
    return service.calcular_multa(idLocacao)

@router.post("/alugar", response_model=LocacaoResponse)
def alugar_filme(dados: AluguelRequest, db: Session = Depends(get_db)):
    service = LocacaoService(db)
    return service.alugar_filme(
        id_cliente=dados.id_cliente,
        id_filme=dados.id_filme,
        quantidade = dados.quantidade,
        data_devolucao=dados.data_devolucao
    )

@router.delete("/{idLocacao}/deletar", status_code=status.HTTP_204_NO_CONTENT)
def deletar_locacao(idLocacao: int, db: Session = Depends(get_db)):
    service = LocacaoService(db)
    service.deletar(idLocacao)


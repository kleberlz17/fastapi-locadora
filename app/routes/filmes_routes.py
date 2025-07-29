from fastapi import APIRouter, Depends, HTTPException, status, Response

from sqlalchemy.orm import Session
from typing import List
from datetime import date

from app.database import get_db
from app.schemas.filmes_create import FilmeCreate
from app.schemas.filmes_response import FilmeResponse
from app.schemas.filmes_update import FilmeUpdate, NovoEstoque, NovaDataLancamento, NovoNomeFilme
from app.models.filmes import Filmes
from app.services.filmes_service import FilmeService

router = APIRouter() #caminho está no init

@router.post("/salvar", status_code=status.HTTP_201_CREATED)
def salvar(filme_create: FilmeCreate, db: Session = Depends(get_db)):
    service = FilmeService(db)
    filme = service.salvar(filme_create)
    return {"id": filme.id_filme}

@router.get("/{id_filme}", response_model=FilmeResponse)
def buscar_por_id(id_filme: int, db: Session = Depends(get_db)):
    service = FilmeService(db)
    return service.buscar_por_id(id_filme)

@router.get("/nome/{nome}", response_model=List[FilmeResponse])
def buscar_por_nome(nome: str, db: Session = Depends(get_db)):
    service = FilmeService(db)
    filmes = service.buscar_por_nome(nome)
    if not filmes:
        raise HTTPException(status_code=404, detail="Filme(s) não encontrado(s)")
    return filmes

@router.get("/dataLancamento/{data_lancamento}", response_model=List[FilmeResponse])
def buscar_por_data_lancamento(data_lancamento: date, db: Session = Depends(get_db)):
    service = FilmeService(db)
    filmes = service.buscar_por_data_lancamento(data_lancamento)
    if not filmes:
        raise HTTPException(status_code=404, detail="Filme(s) não encontrado(s)")
    return filmes

@router.get("/diretor/{diretor}", response_model=List[FilmeResponse])
def buscar_por_diretor(diretor: str, db: Session = Depends(get_db)):
    service = FilmeService(db)
    filmes = service.buscar_por_diretor(diretor)
    if not filmes:
        raise HTTPException(status_code=404, detail="Filme(s) não encontrado(s)")
    return filmes

@router.get("/genero/{genero}", response_model=List[FilmeResponse])
def buscar_por_genero(genero: str, db: Session = Depends(get_db)):
    service = FilmeService(db)
    filmes = service.buscar_por_genero(genero)
    if not filmes:
        raise HTTPException(status_code=404, detail="Filme(s) não encontrado(s)")
    return filmes

@router.put("/{id_filme}/novoEstoque", response_model=FilmeResponse)
def alterar_estoque(id_filme: int, novo_estoque: NovoEstoque, db: Session = Depends(get_db)):
    service = FilmeService(db)
    return service.alterar_estoque(id_filme, novo_estoque.estoque)

@router.put("/{id_filme}/novaDataLancamento", response_model=FilmeResponse)
def alterar_data_lancamento(id_filme: int, nova_data: NovaDataLancamento, db: Session = Depends(get_db)):
    service = FilmeService(db)
    return service.alterar_data_lancamento(id_filme, nova_data.data_lancamento)

@router.put("/{id_filme}/novoNomeFilme", response_model=FilmeResponse)
def alterar_nome_filme(id_filme: int, novo_nome: NovoNomeFilme, db: Session = Depends(get_db)):
    service = FilmeService(db)
    return service.alterar_nome(id_filme, novo_nome.nome)

@router.delete("/{id_filme}/deletar", status_code=status.HTTP_204_NO_CONTENT)
def deletar_filme(id_filme: int, db: Session = Depends(get_db)):
    service = FilmeService(db)
    service.deletar(id_filme)
    return Response(status_code=status.HTTP_204_NO_CONTENT)
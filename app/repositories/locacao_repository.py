from sqlalchemy.orm import Session
from app.models.locacao import Locacao
from app.models.cliente import Cliente
from app.models.filmes import Filmes
from datetime import date

def get_by_id(db: Session, id_locacao: int): ##id da locação
    return db.query(Locacao).filter(Locacao.id_locacao == id_locacao).first() #optional

def get_by_cliente_id(db: Session, cliente_id: int):
    return db.query(Locacao).filter(Locacao.id_cliente == cliente_id).all() #list

def get_by_filme_id(db: Session, filme_id: int):
    return db.query(Locacao).filter(Locacao.id_filme == filme_id).all() #list

def get_by_cliente(db: Session, cliente: Cliente):
    return db.query(Locacao).filter(Locacao.cliente == cliente).all() #list

def get_by_filme(db: Session, filme: Filmes):
    return db.query(Locacao).filter(Locacao.filme == filme).all() #list

def get_by_data_locacao(db: Session, data: date):
    return db.query(Locacao).filter(Locacao.data_locacao == data).all() #list

def get_by_data_devolucao(db: Session, data: date):
    return db.query(Locacao).filter(Locacao.data_devolucao == data).all() #list

def get_by_quantidade(db: Session, quantidade: int):
    return db.query(Locacao).filter(Locacao.quantidade == quantidade).first() #optional

def save(db: Session, locacao: Locacao):
    db.add(locacao)
    db.commit()
    db.refresh(locacao)
    return locacao

def delete(db: Session, locacao: Locacao):
    db.delete(locacao)
    db.commit()

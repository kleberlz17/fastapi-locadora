from sqlalchemy.orm import Session
from app.models.cliente import Cliente


def get_by_id(db: Session, id: int):
    return db.query(Cliente).filter(Cliente.id == id).first() #first é equivalente ao optional(1 na lista)

def get_by_telefone(db: Session, telefone: str):
    return db.query(Cliente).filter(Cliente.telefone == telefone).first() #first é equivalente ao optional(1 na lista)

def get_by_email(db:Session, email: str):
    return db.query(Cliente).filter(Cliente.email == email).first() #first é equivalente ao optional(1 na lista)

def get_by_cpf_ignore_case(db: Session, cpf: str):
    #ilike busca ignorando maiusculas e minusculas
    return db.query(Cliente).filter(Cliente.cpf.ilike(f"%{cpf}%")).first() #first é equivalente ao optional(1 na lista)

def get_by_nome_ignore_case(db: Session, nome: str):
    # ilike busca ignorando maiusculas e minusculas
    return db.query(Cliente).filter(Cliente.nome.ilike(f"%{nome}%")).all() #retorna toda a lista

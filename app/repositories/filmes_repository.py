from sqlalchemy.orm import Session, load_only
from app.models.filmes import Filmes
from datetime import date

def get_by_id(db: Session, id_filme: int): #Não chamar o relacionamento com locação,
    return db.query(Filmes).filter(Filmes.id_filme == id_filme).first()

def get_by_nome_ignore_case(db: Session, nome: str):
    # ilike busca ignorando maiusculas e minusculas
    return db.query(Filmes).filter(Filmes.nome.ilike(nome)).first() #first é equivalente ao optional(1 na lista)

def get_by_nome_contendo(db: Session, nome: str):
    #ESSE BUSCA TODOS OS FILMES QUE CONTENHAM A PALAVRA BUSCADA
    # ilike busca ignorando maiusculas e minusculas
    return db.query(Filmes).filter(Filmes.nome.ilike(f"%{nome}%")).all() #retorna toda a lista

def get_by_data_lancamento(db: Session, data: date):
    return db.query(Filmes).filter(Filmes.data_lancamento == data).all() #retorna toda a lista

def get_by_diretor_contendo(db: Session, diretor: str):
    # ilike busca ignorando maiusculas e minusculas
    return db.query(Filmes).filter(Filmes.diretor.ilike(f"%{diretor}%")).all() #retorna toda a lista

def get_by_genero_contendo(db: Session, genero: str):
    # ilike busca ignorando maiusculas e minusculas
    return db.query(Filmes).filter(Filmes.genero.ilike(f"%{genero}%")).all() #retorna toda a lista

def get_by_estoque(db: Session, estoque: int):
    return db.query(Filmes).filter(Filmes.estoque == estoque).all() #retorna toda a lista

def save(db: Session, filme: Filmes) -> Filmes:
    ## Aqui é pra garantir que todas as locações associadas ao filme estão na sessão do SQLAlchemy,
    ## e garantindo que os relacionamentos estão sendo salvos.
    ## E poderia futuramente ter dados soltos pq a ligação não foi salva corretamente.
    ## Se não colocar os ifs de reafirmação, vai ficar dando warning.
    for locacao in filme.locacoes:
        if locacao not in db:
            db.add(locacao)

    db.add(filme)
    db.commit()
    db.refresh(filme)
    return filme

def delete(db: Session, filme: Filmes):
    db.delete(filme)
    db.commit()
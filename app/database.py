import os

from sqlalchemy import create_engine
from sqlalchemy.orm import declarative_base
from sqlalchemy.orm import sessionmaker

SQLALCHEMY_DATABASE_URL = os.getenv(
    "DATABASE_URL",  ##Se existir variavel com esse nome, usa  ela, se não, usa a local abaixo.
    "postgresql://user:password@localhost:5432/fastapi-locadora"
)

engine = create_engine(SQLALCHEMY_DATABASE_URL)

SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

Base = declarative_base()

##Essa função injeta o Database(db) nos endpoints.
def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()
import logging
import pytest
from fastapi.testclient import TestClient
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from app.database import Base, get_db
from app.main import app

#Loggings pra acompanhar as respostas.
logging.basicConfig(level=logging.INFO, format="%(asctime)s - %(levelname)s - %(message)s")
logger = logging.getLogger(__name__)

SQLALCHEMY_DATABASE_URL = "sqlite:///./test.db"
engine = create_engine(SQLALCHEMY_DATABASE_URL, connect_args={"check_same_thread": False})
TestingSessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

Base.metadata.create_all(bind=engine)

def override_get_db():
    db = TestingSessionLocal()
    try:
        yield db
    finally:
        db.close()

app.dependency_overrides[get_db] = override_get_db
client = TestClient(app)

##Pra limpar o banco de dados conforme os testes ocorrerem..
@pytest.fixture(autouse=True)
def clean_db():
    Base.metadata.drop_all(bind=engine)
    Base.metadata.create_all(bind=engine)
    yield

#Testes de integração filmes routes.
def test_salvar_filme():
    logger.info("Iniciando teste: test_salvar_filme")
    response = client.post("/filmes/salvar", json={
        "nome": "Fantastic Four",
        "data_lancamento": "2025-07-25",
        "diretor": "Matt Shakman",
        "genero": "Super-Heróis",
        "estoque": 2
    })
    logger.info(f"POST /filmes/salvar retornou status {response.status_code}")
    assert response.status_code == 201
    assert "id" in response.json()
    logger.info("Teste test_salvar_filme finalizado com sucesso")

def test_buscar_filme_por_id():
    logger.info("Iniciando teste: test_buscar_filme_por_id")
    filme = client.post("/filmes/salvar", json={
        "nome": "Lilo & Stitch",
        "data_lancamento": "2025-05-22",
        "diretor": "Dean Fleischer Camp",
        "genero": "Infantil",
        "estoque": 1
    }).json()
    response = client.get(f"/filmes/{filme['id']}")
    logger.info(f"GET /filmes/{filme['id']} retornou status {response.status_code}")
    assert response.status_code == 200
    assert response.json()["nome"] == "Lilo & Stitch"
    logger.info("Teste test_buscar_filme_por_id finalizado com sucesso")

def test_buscar_filme_por_nome():
    logger.info("Iniciando teste: test_buscar_filme_por_nome")
    client.post("/filmes/salvar", json={
        "nome": "Beauty and the Beast",
        "data_lancamento": "2017-03-16",
        "diretor": "Bill Condon",
        "genero": "Fantasia",
        "estoque": 2
    })
    response = client.get("/filmes/nome/Beauty")
    logger.info(f"GET /filmes/nome/Beauty retornou status {response.status_code}")
    assert response.status_code == 200
    assert any(c["nome"] == "Beauty and the Beast" for c in response.json())
    logger.info("Teste test_buscar_filme_por_nome finalizado com sucesso")

def test_buscar_por_data_lancamento():
    logger.info("Iniciando teste: test_buscar_por_data_lancamento")
    client.post("/filmes/salvar", json={
        "nome": "A Christmas Carol",
        "data_lancamento": "2009-11-06",
        "diretor": "Robert Zemeckis",
        "genero": "Animação",
        "estoque": 4
    })
    response = client.get("/filmes/dataLancamento/2009-11-06")
    logger.info(f"GET /filmes/dataLancamento/2009-11-06 retornou status {response.status_code}")
    assert response.status_code == 200
    logger.info("Teste test_buscar_por_data_lancamento finalizado com sucesso")

def test_buscar_por_diretor():
    logger.info("Iniciando teste: test_buscar_por_diretor")
    client.post("/filmes/salvar", json={
        "nome": "The Polar Express",
        "data_lancamento": "2004-12-03",
        "diretor": "Robert Zemeckis",
        "genero": "Animação",
        "estoque": 5
    })
    response = client.get("/filmes/diretor/Robert")
    logger.info(f"GET /filmes/diretor/Robert retornou status {response.status_code}")
    assert response.status_code == 200
    assert any(c["diretor"] == "Robert Zemeckis" for c in response.json())
    logger.info("Teste test_buscar_por_diretor finalizado com sucesso")

def test_buscar_por_genero():
    logger.info("Iniciando teste: test_buscar_por_genero")
    client.post("/filmes/salvar", json={
        "nome": "The Butterfly Effect",
        "data_lancamento": "2004-07-23",
        "diretor": "Eric Bress",
        "genero": "Suspense",
        "estoque": 7
    })
    response = client.get("/filmes/genero/suspense")
    logger.info(f"GET /filmes/genero/suspense retornou status {response.status_code}")
    assert response.status_code == 200
    assert any(c["genero"] == "Suspense" for c in response.json())
    logger.info("Teste test_buscar_por_genero finalizado com sucesso")

def test_alterar_estoque():
    logger.info("Iniciando teste: test_alterar_estoque")
    filme = client.post("/filmes/salvar", json={
        "nome": "The Notebook",
        "data_lancamento": "2004-08-13",
        "diretor": "Nick Cassavetes",
        "genero": "Romance",
        "estoque": 6
    }).json()
    response = client.put(f"/filmes/{filme['id']}/novoEstoque", json={"estoque": 7})
    logger.info(f"PUT /filmes/{filme['id']}/novoEstoque retornou status {response.status_code}")
    assert response.status_code == 200
    assert response.json()["estoque"] == 7
    logger.info("Teste test_alterar_estoque finalizado com sucesso")

def test_alterar_data_lancamento():
    logger.info("Iniciando teste: test_alterar_data_lancamento")
    filme = client.post("/filmes/salvar", json={
        "nome": "Hulk",
        "data_lancamento": "2002-03-20",
        "diretor": "Ang Lee",
        "genero": "Super-Herói",
        "estoque": 7
    }).json()
    response = client.put(f"/filmes/{filme['id']}/novaDataLancamento", json={"data_lancamento": "2002-06-27"})
    logger.info(f"PUT /filmes/{filme['id']}/novaDataLancamento retornou status {response.status_code}")
    assert response.status_code == 200
    assert response.json()["data_lancamento"] == "2002-06-27"
    logger.info("Teste test_alterar_data_lancamento finalizado com sucesso")

def test_alterar_nome_filme():
    logger.info("Iniciando teste: test_alterar_nome_filme")
    filme = client.post("/filmes/salvar", json={
        "nome": "Batman",
        "data_lancamento": "2022-03-03",
        "diretor": "Matt Reeves",
        "genero": "Super-Herói",
        "estoque": 1
    }).json()
    response = client.put(f"/filmes/{filme['id']}/novoNomeFilme", json={"nome": "The Batman"})
    logger.info(f"PUT /filmes/{filme['id']}/novoNomeFilme retornou status {response.status_code}")
    assert response.status_code == 200
    assert response.json()["nome"] == "The Batman"
    logger.info("Teste test_alterar_nome_filme finalizado com sucesso")

def test_deletar_filme():
    logger.info("Iniciando teste: test_deletar_filme")
    filme = client.post("/filmes/salvar", json={
        "nome": "Batman Begins",
        "data_lancamento": "2005-06-17",
        "diretor": "Christopher Nolan",
        "genero": "Super-Herói",
        "estoque": 2
    }).json()
    response = client.delete(f"/filmes/{filme['id']}/deletar")
    logger.info(f"DELETE /filmes/{filme['id']}/deletar retornou status {response.status_code}")
    assert response.status_code == 204
    check = client.get(f"/filmes/{filme['id']}")
    logger.info(f"GET /filmes/{filme['id']} após exclusão retornou status {check.status_code}")
    assert check.status_code == 404
    logger.info("Teste test_deletar_filme finalizado com sucesso")

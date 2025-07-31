import logging
import pytest
from fastapi.testclient import TestClient
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from app.database import Base, get_db
from datetime import date
from app.main import app
from app.models.cliente import Cliente
from app.models.filmes import Filmes

#Loggings pra acompanhar as respostas.
logging.basicConfig(level=logging.INFO, format="%(asctime)s - %(levelname)s - %(message)s")
logger = logging.getLogger(__name__)

#Config banco de dados
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

#Variáveis dos IDs
CLIENTE_ID = None
CLIENTE2_ID = None
FILME_ID = None
FILME2_ID = None
LOCACAO_ID = None

#Adicionando Cliente e Filme antes dos testes.
@pytest.fixture(scope="module", autouse=True)
def setup_db():
    global CLIENTE_ID, CLIENTE2_ID, FILME_ID, FILME2_ID
    db = TestingSessionLocal()
    cliente = Cliente(
        nome="Jhon",
        data_nascimento=date(1991, 6,11,),
        cpf="09384726354",
        telefone="999384192",
        email="jhon@email.com",
        endereco="Rua Testar, 33"
    )
    cliente2 = Cliente(
        nome="Alice",
        data_nascimento=date(1994, 4, 19,),
        cpf="34095867543",
        telefone="987444444",
        email="Alice@email.com",
        endereco="Rua Wonderland, 1"
    )
    filme = Filmes(
        nome="Matrix",
        data_lancamento=date(1999, 5, 21),
        diretor="Lana Wachowski",
        genero="Ficção científica",
        estoque=7
    )
    filme2 = Filmes(
        nome="Matrix Reloaded",
        data_lancamento=date(2003, 5, 16),
        diretor="Lilly Wachowski",
        genero="Ficção científica",
        estoque=4
    )
    db.add_all([cliente, cliente2, filme, filme2])
    db.commit()
    db.refresh(cliente); db.refresh(filme)
    db.refresh(cliente2); db.refresh(filme2)

    #Captando os ids do filme e do cliente, pq não tem como saber o ID que vai ser gerado.
    CLIENTE_ID, FILME_ID = cliente.id, filme.id_filme
    CLIENTE2_ID, FILME2_ID = cliente2.id, filme2.id_filme

    yield
    Base.metadata.drop_all(bind=engine) #Limpa banco após testes.

#Testes de integração routes locação
def test_salvar_locacao():
    global LOCACAO_ID
    logger.info("Iniciando teste: test_salvar_locacao")
    locacao = {
        "id_cliente": CLIENTE_ID,
        "id_filme": FILME_ID,
        "data_locacao": "2025-07-30",
        "data_devolucao": "2025-08-05",
        "devolvido": False,
        "quantidade": 1
    }
    response = client.post("/locacao/salvar", json=locacao)
    logger.info(f"Resposta: {response.status_code} - {response.json()}")
    assert response.status_code == 201
    LOCACAO_ID = response.json()["id"] #Pegando o ID real.
    logger.info(f"Locação criada com ID {LOCACAO_ID}")

def test_buscar_locacoes_cliente():
    logger.info("Iniciando teste: test_buscar_locacoes_cliente")
    response = client.get(f"/locacao/{CLIENTE_ID}/locacoes")
    logger.info(f"Resposta: {response.status_code} - {response.json()}")
    assert response.status_code == 200
    data = response.json()
    assert isinstance(data, list)
    assert data[0]["id_cliente"] == CLIENTE_ID

def test_buscar_historico_filme():
    logger.info("Iniciando teste: test_buscar_historico_filme")
    response = client.get(f"/locacao/{FILME_ID}/historico")
    logger.info(f"Resposta: {response.status_code} - {response.json()}")
    assert response.status_code == 200
    data = response.json()
    assert len(data) > 0 # Confere se tem pelo menos 1 dado.

def test_renovar_locacao():
    logger.info("Iniciando teste: test_renovar_locacao")
    renovar = {"data_devolucao": "2025-08-10"}
    response = client.put(f"/locacao/{LOCACAO_ID}/renovarLocacao", json=renovar)
    logger.info(f"Resposta: {response.status_code} - {response.json()}")
    assert response.status_code == 200
    data = response.json()
    assert data["data_devolucao"] == "2025-08-10"

def test_calcular_multa():
    logger.info("Iniciando teste: test_calcular_multa")
    response = client.post(f"/locacao/{LOCACAO_ID}/multa")
    logger.info(f"Resposta: {response.status_code} - {response.json()}")
    assert response.status_code == 200
    assert isinstance(response.json(), float)

def test_alugar_filme():
    logger.info("Iniciando teste: test_alugar_filme")
    locacao = {
        "id_cliente": CLIENTE2_ID,
        "id_filme": FILME2_ID,
        "quantidade": 1,
        "data_devolucao": "2025-08-05"
    }
    response = client.post("/locacao/alugar", json=locacao)
    logger.info(f"Resposta: {response.status_code} - {response.json()}")
    assert response.status_code == 200
    data = response.json()
    assert data["id_cliente"] == CLIENTE2_ID
    assert data["id_filme"] == FILME2_ID

def test_deletar_locacao():
    logger.info("Iniciando teste: test_deletar_locacao")
    response = client.delete(f"/locacao/{LOCACAO_ID}/deletar")
    logger.info(f"Resposta DELETE: {response.status_code}")
    assert response.status_code == 204


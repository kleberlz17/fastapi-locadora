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

##CONFIG do banco de dados pros testes.
SQLALCHEMY_DATABASE_URL = "sqlite:///./test.db"
engine = create_engine(SQLALCHEMY_DATABASE_URL, connect_args={"check_same_thread": False})
TestingSessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

#Tabelas criadas pros testes.
Base.metadata.create_all(bind=engine)

def override_get_db():
    db = TestingSessionLocal()
    try:
        yield db
    finally:
        db.close()

app.dependency_overrides[get_db] = override_get_db
client = TestClient(app)

##Limpar o banco de dados antes de cada teste.
@pytest.fixture(autouse=True)
def clean_db():
    Base.metadata.drop_all(bind=engine)
    Base.metadata.create_all(bind=engine)
    yield

#Testes de integração routes cliente.
def test_salvar_cliente():
    logger.info("Iniciando teste: test_salvar_cliente")
    response = client.post("/clientes/salvar", json={
        "nome": "Junior",
        "data_nascimento": "1999-07-27",
        "cpf": "77777777777",
        "telefone": "999999999",
        "email": "junior@email.com",
        "endereco": "Rua Teste A, 777"
    })
    logger.info(f"POST /clientes/salvar retornou status {response.status_code}")
    assert response.status_code == 201
    assert "id" in response.json()
    logger.info("Teste test_salvar_cliente finalizado com sucesso")

def test_buscar_cliente_por_id():
    logger.info("Iniciando teste: test_buscar_cliente_por_id")
    novo = client.post("/clientes/salvar", json={
        "nome": "Bernardo",
        "data_nascimento": "2004-04-11",
        "cpf": "66666666666",
        "telefone": "444444444",
        "email": "bernardo@email.com",
        "endereco": "Rua Teste B, 777"
    }).json()
    response = client.get(f"/clientes/{novo['id']}")
    logger.info(f"GET /clientes/{novo['id']} retornou status {response.status_code}")
    assert response.status_code == 200
    assert response.json()["nome"] == "Bernardo"
    logger.info("Teste test_buscar_cliente_por_id finalizado com sucesso")

def test_buscar_cliente_por_nome():
    logger.info("Iniciando teste: test_buscar_cliente_por_nome")
    client.post("/clientes/salvar", json={
        "nome": "Mayra",
        "data_nascimento": "1989-02-10",
        "cpf": "55555555555",
        "telefone": "111111111",
        "email": "mayra@email.com",
        "endereco": "Rua Teste C, 777"
    })
    response = client.get("/clientes/nome/Mayra")
    logger.info(f"GET /clientes/nome/Mayra retornou status {response.status_code}")
    assert response.status_code == 200
    assert any(c["nome"] == "Mayra" for c in response.json())
    logger.info("Teste test_buscar_cliente_por_nome finalizado com sucesso")

def test_buscar_cliente_por_cpf():
    logger.info("Iniciando teste: test_buscar_cliente_por_cpf")
    client.post("/clientes/salvar", json={
        "nome": "Bruce",
        "data_nascimento": "1970-01-17",
        "cpf": "99999999999",
        "telefone": "123456789",
        "email": "bruce@email.com",
        "endereco": "Gotham City, subsolo"
    })
    response = client.get("/clientes/cpf/99999999999")
    logger.info(f"GET /clientes/cpf/99999999999 retornou status {response.status_code}")
    assert response.status_code == 200
    assert response.json()["cpf"] == "99999999999"
    logger.info("Teste test_buscar_cliente_por_cpf finalizado com sucesso")

def test_atualizar_cliente():
    logger.info("Iniciando teste: test_atualizar_cliente")
    novo = client.post("/clientes/salvar", json={
        "nome": "Clark",
        "data_nascimento": "1970-02-10",
        "cpf": "33333333333",
        "telefone": "900000000",
        "email": "clark@email.com",
        "endereco": "Metropolis"
    }).json()
    response = client.put(f"/clientes/{novo['id']}", json={
        "nome": "Clark Kent",
        "endereco": "Metropolis, 754"
    })
    logger.info(f"PUT /clientes/{novo['id']} retornou status {response.status_code}")
    assert response.status_code == 200
    assert response.json()["nome"] == "Clark Kent"
    logger.info("Teste test_atualizar_cliente finalizado com sucesso")

def test_alterar_telefone():
    logger.info("Iniciando teste: test_alterar_telefone")
    novo = client.post("/clientes/salvar", json={
        "nome": "Steve",
        "data_nascimento": "1950-01-28",
        "cpf": "77733388866",
        "telefone": "999665533",
        "email": "steve@email.com",
        "endereco": "Washington, D.C"
    }).json()
    response = client.put(f"/clientes/{novo['id']}/novoTelefone", json={"telefone": "112223344"})
    logger.info(f"PUT /clientes/{novo['id']}/novoTelefone retornou status {response.status_code}")
    assert response.status_code == 200
    assert response.json()["telefone"] == "112223344"
    logger.info("Teste test_alterar_telefone finalizado com sucesso")

def test_alterar_email():
    logger.info("Iniciando teste: test_alterar_email")
    novo = client.post("/clientes/salvar", json={
        "nome": "Tony",
        "data_nascimento": "1977-04-12",
        "cpf": "77644892347",
        "telefone": "987456271",
        "email": "tony@email.com",
        "endereco": "New York"
    }).json()
    response = client.put(f"/clientes/{novo['id']}/novoEmail", json={"email": "stark@email.com"})
    logger.info(f"PUT /clientes/{novo['id']}/novoEmail retornou status {response.status_code}")
    assert response.status_code == 200
    assert response.json()["email"] == "stark@email.com"
    logger.info("Teste test_alterar_email finalizado com sucesso")

def test_alterar_endereco():
    logger.info("Iniciando teste: test_alterar_endereco")
    novo = client.post("/clientes/salvar", json={
        "nome": "Wanda",
        "data_nascimento": "1989-03-07",
        "cpf": "99955544728",
        "telefone": "998765309",
        "email": "wanda@email.com",
        "endereco": "Westview, New Jersey"
    }).json()
    response = client.put(f"/clientes/{novo['id']}/novoEndereco", json={"endereco": "Westfield, New Jersey"})
    logger.info(f"PUT /clientes/{novo['id']}/novoEndereco retornou status {response.status_code}")
    assert response.status_code == 200
    assert response.json()["endereco"] == "Westfield, New Jersey"
    logger.info("Teste test_alterar_endereco finalizado com sucesso")

def test_deletar_cliente():
    logger.info("Iniciando teste: test_deletar_cliente")
    novo = client.post("/clientes/salvar", json={
        "nome": "Norman",
        "data_nascimento": "1960-02-11",
        "cpf": "88463729875",
        "telefone": "977777654",
        "email": "osborn@email.com",
        "endereco": "Hartford, Connecticut"
    }).json()
    response = client.delete(f"/clientes/{novo['id']}/deletar")
    logger.info(f"DELETE /clientes/{novo['id']}/deletar retornou status {response.status_code}")
    assert response.status_code == 204
    check = client.get(f"/clientes/{novo['id']}")
    logger.info(f"GET /clientes/{novo['id']} após exclusão retornou status {check.status_code}")
    assert check.status_code == 404
    logger.info("Teste test_deletar_cliente finalizado com sucesso")
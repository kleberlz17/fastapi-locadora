import pytest
from fastapi import HTTPException
from datetime import date
from app.services.cliente_service import ClienteService
from app.schemas.cliente_create import ClienteCreate
from app.schemas.cliente_update import ClienteUpdate
from app.models import Cliente

def cliente_fake():
    cliente = Cliente()
    cliente.id = 1
    cliente.nome = "Kleber Luiz"
    cliente.data_nascimento = date(1999, 10, 10)
    cliente.cpf = "12345678900"
    cliente.telefone = "11999999999"
    cliente.email = "kleber@email.com"
    cliente.endereco = "Rua Tests"
    return cliente

def test_salvar_cliente_com_cpf(mocker):
    db_mock = mocker.MagicMock()
    db_mock.add = mocker.MagicMock()
    db_mock.commit = mocker.MagicMock()

    def refresh_side_effect(obj):
        obj.id = 1
    db_mock.refresh = mocker.MagicMock(side_effect=refresh_side_effect)

    service = ClienteService(db_mock)

    cliente_create = ClienteCreate(
        nome="Junior",
        data_nascimento=date(1999, 11, 13),
        cpf="22222222222",
        telefone="11988888888",
        email="junior@email.com",
        endereco="Rua das ruas"
    )

    response = service.salvar(cliente_create=cliente_create)

    assert response.id == 1
    assert response.nome == "Junior"
    db_mock.add.assert_called_once()
    db_mock.commit.assert_called_once()
    db_mock.refresh.assert_called_once()

def test_buscar_por_id_cliente_existente(mocker):
    db_mock = mocker.MagicMock()
    cliente = cliente_fake()

    query_mock = mocker.MagicMock()
    filter_mock = mocker.MagicMock()
    db_mock.query.return_value = query_mock
    query_mock.filter.return_value = filter_mock
    filter_mock.first.return_value = cliente

    service = ClienteService(db_mock)

    result = service.buscar_por_id(1)

    assert result.id == 1
    assert result.nome == "Kleber Luiz"

def test_buscar_por_cpf_sucesso(mocker):
    db_mock = mocker.MagicMock()
    cliente = cliente_fake()

    query_mock = mocker.MagicMock()
    filter_mock = mocker.MagicMock()
    db_mock.query.return_value = query_mock
    query_mock.filter.return_value = filter_mock
    filter_mock.first.return_value = cliente

    service = ClienteService(db_mock)

    result = service.buscar_por_cpf("12345678900")

    assert result.cpf == "12345678900"

def test_alterar_email_sucesso(mocker):
    db_mock = mocker.MagicMock()
    cliente = cliente_fake()

    query_mock = mocker.MagicMock()
    filter_mock = mocker.MagicMock()
    db_mock.query.return_value = query_mock
    query_mock.filter.return_value = filter_mock
    filter_mock.first.return_value = cliente

    db_mock.commit = mocker.MagicMock()
    db_mock.refresh = mocker.MagicMock()

    service = ClienteService(db_mock)
    mocker.patch.object(service.validator, "validar_email", return_value=None)

    novo_email = "novo@email.com"
    result = service.alterar_email(1, novo_email)

    assert result.email == novo_email
    db_mock.commit.assert_called_once()
    db_mock.refresh.assert_called_once_with(cliente)

def test_alterar_telefone_sucesso(mocker):
    db_mock = mocker.MagicMock()
    cliente = cliente_fake()

    query_mock = mocker.MagicMock()
    filter_mock = mocker.MagicMock()
    db_mock.query.return_value = query_mock
    query_mock.filter.return_value = filter_mock
    filter_mock.first.return_value = cliente

    db_mock.commit = mocker.MagicMock()
    db_mock.refresh = mocker.MagicMock()

    service = ClienteService(db_mock)
    mocker.patch.object(service.validator, "validar_telefone", return_value=None)

    novo_telefone = "11911112222"
    result = service.alterar_telefone(1, novo_telefone)

    assert result.telefone == novo_telefone
    db_mock.commit.assert_called_once()
    db_mock.refresh.assert_called_once_with(cliente)

def test_alterar_endereco_sucesso(mocker):
    db_mock = mocker.MagicMock()
    cliente = cliente_fake()

    query_mock = mocker.MagicMock()
    filter_mock = mocker.MagicMock()
    db_mock.query.return_value = query_mock
    query_mock.filter.return_value = filter_mock
    filter_mock.first.return_value = cliente

    db_mock.commit = mocker.MagicMock()
    db_mock.refresh = mocker.MagicMock()

    service = ClienteService(db_mock)

    novo_endereco = "Rua Nova, 123"
    result = service.alterar_endereco(1, novo_endereco)

    assert result.endereco == novo_endereco
    db_mock.commit.assert_called_once()
    db_mock.refresh.assert_called_once_with(cliente)

def test_atualizar_cliente_sucesso(mocker):
    db_mock = mocker.MagicMock()
    cliente = cliente_fake()

    query_mock = mocker.MagicMock()
    filter_mock = mocker.MagicMock()
    db_mock.query.return_value = query_mock
    query_mock.filter.return_value = filter_mock
    filter_mock.first.return_value = cliente

    db_mock.commit = mocker.MagicMock()
    db_mock.refresh = mocker.MagicMock()

    service = ClienteService(db_mock)

    cliente_update = ClienteUpdate(
        nome="Nome Atualizado",
        telefone="11922223333",
        email="atualizado@email.com",
        endereco="Rua Atualizada"
    )

    result = service.atualizar(1, cliente_update)

    assert result.nome == "Nome Atualizado"
    assert result.telefone == "11922223333"
    assert result.email == "atualizado@email.com"
    assert result.endereco == "Rua Atualizada"
    db_mock.commit.assert_called_once()
    db_mock.refresh.assert_called_once_with(cliente)

def test_deletar_cliente_sucesso(mocker):
    db_mock = mocker.MagicMock()
    cliente = cliente_fake()

    query_mock = mocker.MagicMock()
    filter_mock = mocker.MagicMock()
    db_mock.query.return_value = query_mock
    query_mock.filter.return_value = filter_mock
    filter_mock.first.return_value = cliente

    db_mock.delete = mocker.MagicMock()
    db_mock.commit = mocker.MagicMock()

    service = ClienteService(db_mock)

    result = service.deletar(1)

    db_mock.delete.assert_called_once_with(cliente)
    db_mock.commit.assert_called_once()
    assert result is None

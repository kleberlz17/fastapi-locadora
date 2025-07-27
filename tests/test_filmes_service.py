import pytest
from fastapi import HTTPException
from datetime import date
from app.services.filmes_service import FilmeService
from app.schemas.filmes_create import FilmeCreate
from app.schemas.filmes_update import FilmeUpdate
from app.models import Filmes

def filme_fake():
    filme = Filmes()
    filme.id_filme = 1
    filme.nome = "The Batman"
    filme.data_lancamento = date(2021, 4, 10)
    filme.diretor = "Matt Reeves"
    filme.genero = "Super-Herói"
    filme.estoque = 3
    return filme

def test_salvar_filme(mocker):
    db_mock = mocker.MagicMock()
    db_mock.add = mocker.MagicMock()
    db_mock.commit = mocker.MagicMock()

    def refresh_side_effect(obj):
        obj.id_filme = 2
    db_mock.refresh = mocker.MagicMock(side_effect=refresh_side_effect)

    service = FilmeService(db_mock)

    mocker.patch.object(service.validator, "validar_tudo", return_value=None) #Se não mockar o validator a lógica vai dar erro.

    filmes_create = FilmeCreate(
        nome="Fantastic Four",
        data_lancamento=date(2025, 7, 25),
        diretor="Matt Shakman",
        genero="Super-Herói",
        estoque= 2
    )

    response = service.salvar(filme_create=filmes_create)

    assert response.id_filme == 2
    assert response.nome == "Fantastic Four"
    db_mock.add.assert_called_once()
    db_mock.commit.assert_called_once()
    db_mock.refresh.assert_called_once()

def test_buscar_por_id_filme_existente(mocker):
    db_mock = mocker.MagicMock()
    filme = filme_fake()

    query_mock = mocker.MagicMock()
    filter_mock = mocker.MagicMock()
    db_mock.query.return_value = query_mock
    query_mock.filter.return_value = filter_mock
    filter_mock.first.return_value = filme

    service = FilmeService(db_mock)

    result = service.buscar_por_id(1)

    assert result.id_filme == 1
    assert result.nome == "The Batman"


def test_buscar_por_nome_sucesso(mocker):
    db_mock = mocker.MagicMock()
    filme = filme_fake()

    query_mock = mocker.MagicMock()
    filter_mock = mocker.MagicMock()
    db_mock.query.return_value = query_mock
    query_mock.filter.return_value = filter_mock
    filter_mock.all.return_value = [filme] ##Retorna lista,não o first

    service = FilmeService(db_mock)

    result = service.buscar_por_nome("The Batman")

    assert result[0].nome == "The Batman"

def test_buscar_por_data_lancamento_sucesso(mocker):
    db_mock = mocker.MagicMock()
    filme = filme_fake()

    query_mock = mocker.MagicMock()
    filter_mock = mocker.MagicMock()
    db_mock.query.return_value = query_mock
    query_mock.filter.return_value = filter_mock
    filter_mock.all.return_value = [filme] ##Retorna lista,não o first

    service = FilmeService(db_mock)

    result = service.buscar_por_data_lancamento(date(2021, 4, 10))

    assert result[0].data_lancamento == date(2021, 4, 10)

def test_buscar_por_diretor_sucesso(mocker):
    db_mock = mocker.MagicMock()
    filme = filme_fake()

    query_mock = mocker.MagicMock()
    filter_mock = mocker.MagicMock()
    db_mock.query.return_value = query_mock
    query_mock.filter.return_value = filter_mock
    filter_mock.all.return_value = [filme] ##Retorna lista,não o first

    service = FilmeService(db_mock)

    result = service.buscar_por_diretor("Matt Reeves")

    assert  result[0].diretor == "Matt Reeves"

def test_buscar_por_genero_sucesso(mocker):
    db_mock = mocker.MagicMock()
    filme = filme_fake()

    query_mock = mocker.MagicMock()
    filter_mock = mocker.MagicMock()
    db_mock.query.return_value = query_mock
    query_mock.filter.return_value = filter_mock
    filter_mock.all.return_value = [filme] ##Retorna lista,não o first

    service = FilmeService(db_mock)

    result = service.buscar_por_genero("Super-Herói")

    assert  result[0].genero == "Super-Herói"

def test_buscar_por_estoque_sucesso(mocker):
    db_mock = mocker.MagicMock()
    filme = filme_fake()

    query_mock = mocker.MagicMock()
    filter_mock = mocker.MagicMock()
    db_mock.query.return_value = query_mock
    query_mock.filter.return_value = filter_mock
    filter_mock.all.return_value = [filme] ##Retorna lista,não o first

    service = FilmeService(db_mock)

    result = service.buscar_por_estoque(3)

    assert  result[0].estoque == 3

def test_alterar_estoque_sucesso(mocker):
    db_mock = mocker.MagicMock()
    filme = filme_fake()

    query_mock = mocker.MagicMock()
    filter_mock = mocker.MagicMock()
    db_mock.query.return_value = query_mock
    query_mock.filter.return_value = filter_mock
    filter_mock.first.return_value = filme

    db_mock.commit = mocker.MagicMock()
    db_mock.refresh = mocker.MagicMock()

    service = FilmeService(db_mock)
    mocker.patch.object(service.validator, "validar_estoque", return_value=None) #Se não mockar o validator a lógica vai dar erro.

    novo_estoque = 7
    result = service.alterar_estoque(1, novo_estoque)

    assert result.estoque == novo_estoque
    db_mock.commit.assert_called_once()
    db_mock.refresh.assert_called_once_with(filme)

def test_alterar_data_lancamento_sucesso(mocker):
    db_mock = mocker.MagicMock()
    filme = filme_fake()

    query_mock = mocker.MagicMock()
    filter_mock = mocker.MagicMock()
    db_mock.query.return_value = query_mock
    query_mock.filter.return_value = filter_mock
    filter_mock.first.return_value = filme

    db_mock.commit = mocker.MagicMock()
    db_mock.refresh = mocker.MagicMock()

    service = FilmeService(db_mock)
    mocker.patch.object(service.validator, "validar_data_lancamento", return_value=None) #Se não mockar o validator a lógica vai dar erro.

    nova_data = date(2025, 1, 1)
    result = service.alterar_data_lancamento(1, date(2025, 1, 1))

    assert result.data_lancamento == nova_data
    db_mock.commit.assert_called_once()
    db_mock.refresh.assert_called_once_with(filme)

def test_alterar_nome_sucesso(mocker):
    db_mock = mocker.MagicMock()
    filme = filme_fake()

    query_mock = mocker.MagicMock()
    filter_mock = mocker.MagicMock()
    db_mock.query.return_value = query_mock
    query_mock.filter.return_value = filter_mock
    filter_mock.first.return_value = filme

    db_mock.commit = mocker.MagicMock()
    db_mock.refresh = mocker.MagicMock()

    service = FilmeService(db_mock)
    mocker.patch.object(service.validator, "validar_duplicidade_nome", return_value=None) #Se não mockar o validator a lógica vai dar erro.

    novo_nome = "O Batman"
    result = service.alterar_nome(1, novo_nome)

    assert result.nome == novo_nome
    db_mock.commit.assert_called_once()
    db_mock.refresh.assert_called_once_with(filme)

def test_deletar_filme_sucesso(mocker):
    db_mock = mocker.MagicMock()
    filme = filme_fake()

    query_mock = mocker.MagicMock()
    filter_mock = mocker.MagicMock()
    db_mock.query.return_value = query_mock
    query_mock.filter.return_value = filter_mock
    filter_mock.first.return_value = filme

    db_mock.delete = mocker.MagicMock()
    db_mock.commit = mocker.MagicMock()

    service = FilmeService(db_mock)

    result = service.deletar(1)

    db_mock.delete.assert_called_once_with(filme)
    db_mock.commit.assert_called_once()
    assert result is None




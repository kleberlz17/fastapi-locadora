import logging
import pytest
from fastapi import HTTPException
from datetime import date
from app.services.filmes_service import FilmeService
from app.schemas.filmes_create import FilmeCreate
from app.schemas.filmes_update import FilmeUpdate
from app.models import Filmes

#Loggings pra acompanhar as respostas.
logging.basicConfig(level=logging.INFO, format="%(asctime)s - %(levelname)s - %(message)s")
logger = logging.getLogger(__name__)

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
    logger.info("Iniciando teste: test_salvar_filme")

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
    logger.info(f"Filme salvo: {response}")

    assert response.id_filme == 2
    assert response.nome == "Fantastic Four"
    db_mock.add.assert_called_once()
    db_mock.commit.assert_called_once()
    db_mock.refresh.assert_called_once()
    logger.info("Teste test_salvar_filme finalizado com sucesso")

def test_buscar_por_id_filme_existente(mocker):
    logger.info("Iniciando teste: test_buscar_por_id_filme_existente")

    db_mock = mocker.MagicMock()
    filme = filme_fake()

    query_mock = mocker.MagicMock()
    filter_mock = mocker.MagicMock()
    db_mock.query.return_value = query_mock
    query_mock.filter.return_value = filter_mock
    filter_mock.first.return_value = filme

    service = FilmeService(db_mock)
    result = service.buscar_por_id(1)

    logger.info(f"Resultado obtido: {result}")
    assert result.id_filme == 1
    assert result.nome == "The Batman"
    logger.info("Teste test_buscar_por_id_filme_existente finalizado com sucesso")


def test_buscar_por_nome_sucesso(mocker):
    logger.info("Iniciando teste: test_buscar_por_nome_sucesso")

    db_mock = mocker.MagicMock()
    filme = filme_fake()

    query_mock = mocker.MagicMock()
    filter_mock = mocker.MagicMock()
    db_mock.query.return_value = query_mock
    query_mock.filter.return_value = filter_mock
    filter_mock.all.return_value = [filme] ##Retorna lista,não o first

    service = FilmeService(db_mock)
    result = service.buscar_por_nome("The Batman")

    logger.info(f"Resultado: {result}")
    assert result[0].nome == "The Batman"
    logger.info("Teste test_buscar_por_nome_sucesso finalizado com sucesso")

def test_buscar_por_data_lancamento_sucesso(mocker):
    logger.info("Iniciando teste: test_buscar_por_data_lancamento_sucesso")

    db_mock = mocker.MagicMock()
    filme = filme_fake()

    query_mock = mocker.MagicMock()
    filter_mock = mocker.MagicMock()
    db_mock.query.return_value = query_mock
    query_mock.filter.return_value = filter_mock
    filter_mock.all.return_value = [filme] ##Retorna lista,não o first

    service = FilmeService(db_mock)
    result = service.buscar_por_data_lancamento(date(2021, 4, 10))

    logger.info(f"Resultado: {result}")
    assert result[0].data_lancamento == date(2021, 4, 10)
    logger.info("Teste test_buscar_por_data_lancamento_sucesso finalizado com sucesso")

def test_buscar_por_diretor_sucesso(mocker):
    logger.info("Iniciando teste: test_buscar_por_diretor_sucesso")

    db_mock = mocker.MagicMock()
    filme = filme_fake()

    query_mock = mocker.MagicMock()
    filter_mock = mocker.MagicMock()
    db_mock.query.return_value = query_mock
    query_mock.filter.return_value = filter_mock
    filter_mock.all.return_value = [filme] ##Retorna lista,não o first

    service = FilmeService(db_mock)
    result = service.buscar_por_diretor("Matt Reeves")

    logger.info(f"Resultado: {result}")
    assert  result[0].diretor == "Matt Reeves"
    logger.info("Teste test_buscar_por_diretor_sucesso finalizado com sucesso")

def test_buscar_por_genero_sucesso(mocker):
    logger.info("Iniciando teste: test_buscar_por_genero_sucesso")

    db_mock = mocker.MagicMock()
    filme = filme_fake()

    query_mock = mocker.MagicMock()
    filter_mock = mocker.MagicMock()
    db_mock.query.return_value = query_mock
    query_mock.filter.return_value = filter_mock
    filter_mock.all.return_value = [filme] ##Retorna lista,não o first

    service = FilmeService(db_mock)
    result = service.buscar_por_genero("Super-Herói")

    logger.info(f"Resultado: {result}")
    assert  result[0].genero == "Super-Herói"
    logger.info("Teste test_buscar_por_genero_sucesso finalizado com sucesso")

def test_buscar_por_estoque_sucesso(mocker):
    logger.info("Iniciando teste: test_buscar_por_estoque_sucesso")

    db_mock = mocker.MagicMock()
    filme = filme_fake()

    query_mock = mocker.MagicMock()
    filter_mock = mocker.MagicMock()
    db_mock.query.return_value = query_mock
    query_mock.filter.return_value = filter_mock
    filter_mock.all.return_value = [filme] ##Retorna lista,não o first

    service = FilmeService(db_mock)
    result = service.buscar_por_estoque(3)

    logger.info(f"Resultado: {result}")
    assert  result[0].estoque == 3
    logger.info("Teste test_buscar_por_estoque_sucesso finalizado com sucesso")

def test_alterar_estoque_sucesso(mocker):
    logger.info("Iniciando teste: test_alterar_estoque_sucesso")

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

    logger.info(f"Estoque atualizado para: {result.estoque}")
    assert result.estoque == novo_estoque
    db_mock.commit.assert_called_once()
    db_mock.refresh.assert_called_once_with(filme)
    logger.info("Teste test_alterar_estoque_sucesso finalizado com sucesso")

def test_alterar_data_lancamento_sucesso(mocker):
    logger.info("Iniciando teste: test_alterar_data_lancamento_sucesso")

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

    logger.info(f"Data de lançamento atualizada para: {result.data_lancamento}")
    assert result.data_lancamento == nova_data
    db_mock.commit.assert_called_once()
    db_mock.refresh.assert_called_once_with(filme)
    logger.info("Teste test_alterar_data_lancamento_sucesso finalizado com sucesso")

def test_alterar_nome_sucesso(mocker):
    logger.info("Iniciando teste: test_alterar_nome_sucesso")

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

    logger.info(f"Nome atualizado para: {result.nome}")
    assert result.nome == novo_nome
    db_mock.commit.assert_called_once()
    db_mock.refresh.assert_called_once_with(filme)
    logger.info("Teste test_alterar_nome_sucesso finalizado com sucesso")

def test_deletar_filme_sucesso(mocker):
    logger.info("Iniciando teste: test_deletar_filme_sucesso")

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

    logger.info("Cliente deletado com sucesso")
    db_mock.delete.assert_called_once_with(filme)
    db_mock.commit.assert_called_once()
    assert result is None
    logger.info("Teste test_deletar_filme_sucesso finalizado com sucesso")




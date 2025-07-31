import logging
import pytest
from fastapi import HTTPException
from datetime import date, timedelta
from app.services.locacao_service import LocacaoService
from app.models.locacao import Locacao
from app.models.cliente import Cliente
from app.models.filmes import Filmes
from app.schemas.locacao_create import LocacaoCreate

#Loggings pra acompanhar as respostas.
logging.basicConfig(level=logging.INFO, format="%(asctime)s - %(levelname)s - %(message)s")
logger = logging.getLogger(__name__)

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

def filme_fake():
    filme = Filmes()
    filme.id_filme = 1
    filme.nome = "The Batman"
    filme.data_lancamento = date(2021, 4, 10)
    filme.diretor = "Matt Reeves"
    filme.genero = "Super-Herói"
    filme.estoque = 3
    return filme

def locacao_fake():
    locacao = Locacao()
    locacao.id_locacao = 1
    locacao.id_cliente = 1
    locacao.id_filme = 1
    locacao.data_locacao = date.today()
    locacao.data_devolucao = date(2025, 7, 29)
    locacao.devolvido = False
    locacao.quantidade = 1
    return locacao

def test_salvar_locacao_sucesso(mocker):
    logger.info("Iniciando teste: test_salvar_locacao_sucesso")

    db_mock = mocker.MagicMock()
    cliente = cliente_fake()
    filme = filme_fake()
    locacao = locacao_fake()

    ##mockando todos os metodos do repositories e validator necessários pra lógica.

    mocker.patch("app.services.locacao_service.cliente_repository.get_by_id", return_value=cliente)
    mocker.patch("app.services.locacao_service.filmes_repository.get_by_id", return_value=filme)
    mocker.patch("app.services.locacao_service.filmes_repository.save", return_value=filme)
    mocker.patch("app.services.locacao_service.locacao_repository.save", return_value=locacao)
    mocker.patch("app.services.locacao_service.LocacaoValidator.validar_tudo", return_value=None)

    service = LocacaoService(db_mock)
    locacao_create = LocacaoCreate(
        id_cliente=1,
        id_filme=1,
        data_locacao=date.today(),
        data_devolucao=date(2025, 7, 30),
        devolvido=False,
        quantidade=1
    )

    result = service.salvar(locacao_create)

    logger.info(f"Resultado obtido: {result}")
    assert result.id_locacao == 1
    assert filme.estoque == 2 #Simulando a diminuição do estoque
    logger.info("Iniciando teste: test_salvar_locacao_sucesso finalizado com sucesso")

def test_buscar_por_id_sucesso(mocker):
    logger.info("Iniciando teste: test_buscar_por_id_sucesso")

    db_mock = mocker.MagicMock()
    locacao = locacao_fake()

    mocker.patch("app.services.locacao_service.locacao_repository.get_by_id", return_value=locacao)

    service = LocacaoService(db_mock)
    result = service.buscar_por_id(1)

    logger.info(f"Resultado: {result}")
    assert result.id_locacao == 1
    logger.info("Teste test_buscar_por_id_sucesso finalizado com sucesso")

def test_buscar_por_cliente_id_sucesso(mocker):##Locações do cliente pelo ID.
    logger.info("Iniciando teste: test_buscar_por_cliente_id_sucesso")

    db_mock = mocker.MagicMock()
    locacoes = [locacao_fake()] #Possível lista, embora aqui não venha mais de 1.

    mocker.patch("app.services.locacao_service.locacao_repository.get_by_cliente_id", return_value=locacoes)

    service = LocacaoService(db_mock)
    result = service.buscar_por_cliente_id(1)

    logger.info(f"Resultado: {result}")
    assert result[0].id_cliente == 1
    logger.info("Teste test_buscar_por_cliente_id_sucesso finalizado com sucesso")

def test_buscar_por_filme_id_sucesso(mocker):
    logger.info("Iniciando teste: test_buscar_por_filme_id_sucesso")

    db_mock = mocker.MagicMock()
    locacoes = [locacao_fake()] #Possível lista, embora aqui não venha mais de 1.

    mocker.patch("app.services.locacao_service.locacao_repository.get_by_filme_id", return_value=locacoes)

    service = LocacaoService(db_mock)
    result = service.buscar_por_filme_id(1)

    logger.info(f"Resultado: {result}")
    assert result[0].id_filme == 1
    logger.info("Teste test_buscar_por_filme_id_sucesso finalizado com sucesso")

def test_renovar_data_devolucao_sucesso(mocker):
    logger.info("Iniciando teste: test_renovar_data_devolucao_sucesso")

    db_mock = mocker.MagicMock()
    locacao = locacao_fake()
    nova_data = date.today() + timedelta(days=7) #Simulando acréscimo de 1 semana.

    mocker.patch.object(LocacaoService, "buscar_por_id", return_value=locacao)
    mocker.patch("app.services.locacao_service.locacao_repository.save", return_value=locacao)
    mocker.patch("app.services.locacao_service.LocacaoValidator.validar_data_devolucao", return_value=None)

    service = LocacaoService(db_mock)
    result = service.renovar_data_devolucao(1, nova_data)

    logger.info(f"Data de devolução renovada para: {result.data_devolucao}")
    assert result.data_devolucao == nova_data
    logger.info("Teste test_renovar_data_devolucao_sucesso finalizado com sucesso")

def test_calcular_multa_sucesso(mocker):
    logger.info("Iniciando teste: test_calcular_multa_sucesso")

    db_mock = mocker.MagicMock()
    locacao = locacao_fake()
    locacao.data_devolucao = date.today() + timedelta(days=10) # Simulando atraso de 10 dias.
    logger.info(f"Simulando locação com atraso: data_devolucao={locacao.data_devolucao}")

    mocker.patch.object(LocacaoService, "buscar_por_id", return_value=locacao)

    service = LocacaoService(db_mock)
    multa = service.calcular_multa(1)
    logger.info(f"Multa calculada: {multa}")
    logger.info("Teste test_calcular_multa_sucesso finalizado com sucesso")

def test_alugar_filme_sucesso(mocker):
    logger.info("Iniciando teste: test_alugar_filme_sucesso")

    db_mock = mocker.MagicMock()
    cliente = cliente_fake()
    filme = filme_fake()
    locacao = locacao_fake()

    mocker.patch("app.services.locacao_service.cliente_repository.get_by_id", return_value=cliente)
    mocker.patch("app.services.locacao_service.filmes_repository.get_by_id", return_value=filme)
    mocker.patch("app.services.locacao_service.filmes_repository.save", return_value=filme)
    mocker.patch("app.services.locacao_service.locacao_repository.save", return_value=locacao)
    mocker.patch("app.services.locacao_service.LocacaoValidator.validar_tudo", return_value=None)

    service = LocacaoService(db_mock)
    result = service.alugar_filme(1, 1, 1, date.today())

    logger.info(f"Resultado: {result}")
    assert result.id_locacao == 1
    assert filme.estoque == 2 #Simulando redução do estoque.
    logger.info("Teste test_alugar_filme_sucesso finalizado com sucesso")

def test_deletar_locacao_sucesso(mocker):
    logger.info("Iniciando teste: test_deletar_locacao_sucesso")

    db_mock = mocker.MagicMock()
    locacao = locacao_fake()

    mocker.patch.object(LocacaoService, "buscar_por_id", return_value=locacao)
    delete_mock = mocker.patch("app.services.locacao_service.locacao_repository.delete", return_value=None)

    service = LocacaoService(db_mock)
    service.deletar(1)

    logger.info("Locação deletada com sucesso")
    delete_mock.assert_called_once_with(db_mock, locacao)
    logger.info("Teste test_deletar_locacao_sucesso finalizado com sucesso")




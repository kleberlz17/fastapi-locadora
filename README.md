# 🎬 API de Locadora de Filmes (FastAPI)

API REST desenvolvida em Python 3.11 com FastAPI, que simula o funcionamento de uma locadora de filmes, permitindo o gerenciamento de filmes, clientes e locações, incluindo devoluções e cálculo de multas.

A aplicação está containerizada com Docker e hospedada na AWS, utilizando Amazon EC2 para execução da API e Amazon RDS com PostgreSQL para persistência dos dados.

## 🌐 API Online

A API está atualmente hospedada na AWS e pode ser acessada através da documentação interativa:

- **Swagger UI:** http://18.234.141.156:8000/docs
- **ReDoc:** http://18.234.141.156:8000/redoc

> O endereço da aplicação pode ser alterado futuramente devido à utilização do IPv4 público da instância EC2.

## ✅ Funcionalidades

- Criação e gerenciamento de filmes
- Cadastro e atualização de clientes
- Realização de locações de filmes para clientes
- Devolução de filmes com cálculo automático de multa em caso de atraso
- Consulta de locações por cliente ou por filme
- Consulta de todos os filmes e clientes
- Validações com Pydantic e regras de negócio na camada de serviço
- Conversão entre esquemas Pydantic (DTOs) e modelos ORM
- Testes unitários e de integração com pytest

## 🛠️ Tecnologias e Ferramentas

- Python 3.11
- FastAPI 0.95.1
- SQLAlchemy 2.0.20
- PostgreSQL
- psycopg2-binary 2.9.6
- Pydantic 1.10.12
- Uvicorn 0.22.0
- Docker
- AWS EC2
- AWS RDS
- pytest 7.4.4
- pytest-mock 3.12.0
- httpx 0.27.0

## ☁️ Deploy na AWS

A aplicação foi implantada na AWS utilizando a seguinte arquitetura:

- API FastAPI executada em um container Docker em uma instância Amazon EC2
- Banco de dados PostgreSQL hospedado no Amazon RDS
- Comunicação entre EC2 e RDS configurada através de Security Groups
- Banco de dados sem exposição pública direta
- Credenciais e configurações de conexão fornecidas à aplicação através de variáveis de ambiente
- Container configurado para reinicialização automática

### Arquitetura

Internet → EC2 → Docker → FastAPI → SQLAlchemy → PostgreSQL (RDS)

## 📚 Documentação

O FastAPI gera automaticamente duas interfaces para visualização e teste dos endpoints:

### Ambiente hospedado

- Swagger UI: http://18.234.141.156:8000/docs
- ReDoc: http://18.234.141.156:8000/redoc

### Ambiente local

- Swagger UI: http://localhost:8000/docs
- ReDoc: http://localhost:8000/redoc

## 🚀 Observações

- A API não possui autenticação, sendo um projeto focado na prática de desenvolvimento de APIs REST e arquitetura Back-End.
- No ambiente hospedado, a aplicação e o banco de dados são executados separadamente utilizando EC2 e RDS.
- As credenciais do banco de dados não são armazenadas no código-fonte.
- O arquivo `.env` utilizado para configurações de ambiente não é versionado no repositório.
# 🎬 API de Locadora de Filmes (FastAPI)

API desenvolvida em Python 3.11 com FastAPI, que simula uma locadora de filmes, permitindo o cadastro de filmes, clientes, locação de filmes e cálculo de multas.

✅ **Funcionalidades**
- Criação e gerenciamento de filmes
- Cadastro e atualização de clientes
- Realização de locações de filmes para clientes
- Devolução de filmes com cálculo automático de multa em caso de atraso
- Consulta de locações por cliente ou por filme
- Consulta de todos os filmes e clientes
- Validações com Pydantic e regras de negócio no serviço
- Conversão entre esquemas Pydantic (DTOs) e modelos ORM
- Testes unitários e de integração com pytest

🛠️ **Tecnologias e Ferramentas**
- Python 3.11
- FastAPI 0.95.1
- SQLAlchemy 2.0.20
- PostgreSQL (via psycopg2-binary 2.9.6)
- Pydantic 1.10.12
- Uvicorn 0.22.0
- pytest 7.4.4, pytest-mock 3.12.0, httpx 0.27.0 (para testes)

🚀 **Observações**
- API não possui autenticação, focada no aprendizado e prática de desenvolvimento de APIs REST com FastAPI.
- Documentação interativa automática gerada pelo FastAPI disponível em:
  - http://localhost:8000/docs (Swagger UI)
  - http://localhost:8000/redoc (ReDoc)

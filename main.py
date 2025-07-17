from fastapi import FastAPI
# FastAPI só precisa dos routers aqui, mas ainda não construí nenhum router.
# Os módulos só são importados se eu precisar deles (ex: repositórios, DTOs etc.).
app = FastAPI(
    title="FastAPI Locadora",
    description="API para gerenciamento de locadora de filmes e clientes.",
    version="0.0.1"
)


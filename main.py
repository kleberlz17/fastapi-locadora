from fastapi import FastAPI
from app.routes import router as routes
# FastAPI só precisa dos routes aqui, mas ainda não construí nenhum router.
# Os módulos só são importados se eu precisar deles (ex: repositórios, DTOs etc.).
app = FastAPI(
    title="FastAPI Locadora",
    description="API para gerenciamento de locadora de filmes e clientes.",
    version="1.0.0"
)

app.include_router(routes)


from fastapi import APIRouter
from .cliente_routes import router as cliente_router
from .filmes_routes import router as filmes_router
from .locacao_routes import router as locacao_router

router = APIRouter()
#Aqui devo incluir todas as routes(controllers) que a API terá.
router.include_router(cliente_router, prefix="/clientes", tags=["Clientes"])
router.include_router(filmes_router, prefix="/filmes", tags=["Filmes"])
router.include_router(locacao_router, prefix="/locacao", tags=["Locação"])

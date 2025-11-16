from fastapi import APIRouter
from .auth import router as auth_router
from .enterprises import router as enterprises_router
from .demands import router as demands_router
from .recommendations import router as recommendations_router

api_router = APIRouter()

api_router.include_router(auth_router)
api_router.include_router(enterprises_router)
api_router.include_router(demands_router)
api_router.include_router(recommendations_router)

__all__ = ["api_router"]

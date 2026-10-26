from fastapi import APIRouter
from app.api.v1.health import router as health_router
from app.api.v1.analyze import router as analyze_router
from app.api.v1.explain import router as explain_router

api_router = APIRouter()
api_router.include_router(health_router, tags=["Health"])
api_router.include_router(analyze_router, tags=["Scam Analysis"])
api_router.include_router(explain_router, tags=["AI Explanation"])

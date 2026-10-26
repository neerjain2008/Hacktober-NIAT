from datetime import datetime, timezone
from fastapi import APIRouter
from app.config import settings
from app.services.ollama_client import ollama_client

router = APIRouter()


@router.get("/health", summary="Backend & Ollama Health Status")
async def get_health():
    """Returns service health status and detected local Ollama models."""
    ollama_info = await ollama_client.check_health()
    return {
        "status": "healthy",
        "service": settings.PROJECT_NAME,
        "version": settings.VERSION,
        "ollama": ollama_info,
        "timestamp": datetime.now(timezone.utc).isoformat(),
    }

"""
Vercel FastAPI entrypoint for ScamShield OSS Backend.
Exposes the FastAPI `app` instance from `app.main`.
"""
from app.main import app

__all__ = ["app"]

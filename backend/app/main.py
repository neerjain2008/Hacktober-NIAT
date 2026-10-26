from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from app.config import settings
from app.api.v1.router import api_router
from app.api.v1.explain import router as explain_compat_router

app = FastAPI(
    title=settings.PROJECT_NAME,
    version=settings.VERSION,
    description="Privacy-first, zero-log open-source scam intelligence engine powered by deterministic heuristics and local AI.",
    docs_url="/docs",
    redoc_url="/redoc",
)

# Enable Cross-Origin Resource Sharing (CORS) for Next.js frontend
app.add_middleware(
    CORSMiddleware,
    allow_origins=settings.CORS_ORIGINS,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Mount API v1 router
app.include_router(api_router, prefix=settings.API_V1_STR)

# Also mount /api/explain directly for seamless drop-in parity with Next.js frontend
app.include_router(explain_compat_router, prefix="/api")


@app.get("/", tags=["Root"])
async def root():
    return {
        "service": settings.PROJECT_NAME,
        "version": settings.VERSION,
        "docs": "/docs",
        "api_v1": f"{settings.API_V1_STR}",
        "status": "operational",
    }

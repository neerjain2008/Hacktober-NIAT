import os
from typing import List
from dotenv import load_dotenv

load_dotenv()


class Settings:
    PROJECT_NAME: str = "ScamShield OSS Backend"
    VERSION: str = "1.0.0"
    API_V1_STR: str = "/api/v1"

    # Ollama Local Service Configuration
    OLLAMA_BASE_URL: str = os.getenv("OLLAMA_BASE_URL", "http://localhost:11434")
    DEFAULT_MODEL: str = os.getenv("DEFAULT_MODEL", "gemma4:e2b")
    OLLAMA_TIMEOUT_SECONDS: float = float(os.getenv("OLLAMA_TIMEOUT_SECONDS", "20.0"))
    OLLAMA_TAGS_TIMEOUT_SECONDS: float = float(os.getenv("OLLAMA_TAGS_TIMEOUT_SECONDS", "1.5"))

    # CORS settings
    CORS_ORIGINS: List[str] = [
        "http://localhost:3000",
        "http://127.0.0.1:3000",
        "http://localhost:8000",
        "http://127.0.0.1:8000",
        "*",
    ]


settings = Settings()

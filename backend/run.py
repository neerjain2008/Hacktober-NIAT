import uvicorn
import os

if __name__ == "__main__":
    port = int(os.getenv("PORT", "8000"))
    host = os.getenv("HOST", "0.0.0.0")
    print(f"🛡️  Starting ScamShield OSS Python Backend on http://{host}:{port}")
    print(f"📖 Swagger OpenAPI Docs: http://localhost:{port}/docs")
    uvicorn.run("app.main:app", host=host, port=port, reload=True)

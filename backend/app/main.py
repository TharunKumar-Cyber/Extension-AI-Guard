from fastapi import FastAPI

from backend.app.api.auth import router as auth_router
from backend.app.api.routes import router
from backend.app.core.config import settings


app = FastAPI(
    title=settings.app_name,
    description="AI-powered browser extension security analysisplatform",
    version=settings.app_version,
)

app.include_router(router)
app.include_router(auth_router)


@app.get("/")
def root():
    return {
        "project": settings.app_name,
        "status": "running",
        "version": settings.app_version,
    }


@app.get("/health")
def health():
    return {
        "status": "healthy",
    }

from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from backend.app.api.aegis import router as aegis_router
from backend.app.api.auth import router as auth_router
from backend.app.api.dashboard import router as dashboard_router
from backend.app.api.routes import router
from backend.app.core.config import settings
from backend.app.core.database import initialize_database

initialize_database()

app = FastAPI(
    title=settings.app_name,
    description="AI-powered browser extension security analysis platform",
    version=settings.app_version,
)

app.add_middleware(
    CORSMiddleware,
    allow_origins=[
        "http://127.0.0.1:5173",
        "http://localhost:5173",
    ],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

app.include_router(router)
app.include_router(auth_router)
app.include_router(aegis_router)
app.include_router(dashboard_router)


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

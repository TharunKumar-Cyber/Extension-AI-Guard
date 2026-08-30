from fastapi import APIRouter


router = APIRouter(
    prefix="/api",
    tags=["General"],
)


@router.get("/status")
def status():
    return {
        "status": "online",
        "service": "Extension AI Guard API",
    }
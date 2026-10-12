from fastapi import APIRouter

router = APIRouter()


@router.get("/health")
def health_check():
    from app.core.config import get_settings

    settings = get_settings()
    return {
        "status": "ok",
        "app": settings.app_name,
        "environment": settings.environment,
    }

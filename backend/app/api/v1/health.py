from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session
from sqlalchemy import text
from app.core.database import get_db
from app.core.config import settings
from app.schemas.health import HealthResponse

router = APIRouter()


@router.get("/health", response_model=HealthResponse)
def health_check(db: Session = Depends(get_db)):
    """Comprehensive system health check."""
    db_status = "disconnected"
    try:
        db.execute(text("SELECT 1"))
        db_status = "connected"
    except Exception as e:
        db_status = f"error: {str(e)}"

    return HealthResponse(
        status="healthy" if db_status == "connected" else "degraded",
        app_name=settings.APP_NAME,
        environment=settings.ENVIRONMENT,
        database=db_status,
        version="1.0.0",
        details={
            "embedding_model": settings.EMBEDDING_MODEL,
            "ollama_enabled": settings.ENABLE_OLLAMA,
            "max_upload_size_mb": settings.MAX_UPLOAD_SIZE_MB,
            "rate_limit_per_minute": settings.RATE_LIMIT_PER_MINUTE
        }
    )


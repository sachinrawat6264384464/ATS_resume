import logging
from app.core.config import settings

logger = logging.getLogger("resumeiq.celery")

try:
    from celery import Celery

    celery_app = Celery(
        "resumeiq_worker",
        broker=settings.REDIS_URL,
        backend=settings.REDIS_URL,
    )

    celery_app.conf.update(
        task_serializer="json",
        accept_content=["json"],
        result_serializer="json",
        timezone="UTC",
        enable_utc=True,
        task_track_started=True,
        worker_prefetch_multiplier=1,
    )

    @celery_app.task(name="run_ats_analysis_task", bind=True, max_retries=2)
    def run_ats_analysis_task(self, analysis_id: str, resume_id: str, job_id: str):
        """Celery worker task that executes the LangGraph ATS pipeline."""
        from app.api.v1.analysis import run_pipeline_sync
        logger.info(f"Celery worker received analysis job: {analysis_id}")
        run_pipeline_sync(analysis_id, resume_id, job_id)
        return {"status": "completed", "analysis_id": analysis_id}

except ImportError:
    celery_app = None
    logger.info("Celery is not installed. Using FastAPI in-process BackgroundTasks.")

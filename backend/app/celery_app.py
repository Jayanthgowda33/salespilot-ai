"""
Celery lets us run slow jobs (like re-scoring every lead) in the
background instead of blocking an API request. Start a worker with:
    celery -A app.celery_app worker --loglevel=info
(needs Redis running first — see docker-compose.yml)
"""

from celery import Celery
from app.config import settings

celery_app = Celery("salespilot", broker=settings.REDIS_URL, backend=settings.REDIS_URL)

celery_app.conf.update(
    task_serializer="json",
    result_serializer="json",
    accept_content=["json"],
)

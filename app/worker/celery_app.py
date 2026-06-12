from celery import Celery
from celery.schedules import crontab

celery_app = Celery(
    "worker",
    broker="memory://",
    backend="cache+memory://",
    include=["app.worker.tasks"],
)

celery_app.conf.beat_schedule = {
    "reporting": {
        "task": "app.worker.tasks.reporting",
        "schedule": crontab(minute=0, hour= 7),
    },
}

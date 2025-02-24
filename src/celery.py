from celery.schedules import crontab
from celery import Celery

c_app = Celery("celery")
c_app.config_from_object("src.config")

c_app.conf.beat_schedule = {
    "check-investments-every-5-mins": {
        "task": "src.celery_tasks.check_investments",  # Correct task name
        "schedule": crontab(minute="*/2"),  # Runs every 5 minutes
    },
}

c_app.conf.timezone = "UTC"  # Ensure Celery uses correct timezone

from celery.schedules import crontab
from celery import Celery

# create a celery client which connects to redis server
c_app = Celery("celery")
c_app.config_from_object("src.config")

# celery beat config
c_app.conf.beat_schedule = {
    "check-investments-every-hour": {
        "task": "src.celery_tasks.check_investments",  # Correct task name
        "schedule": crontab(minute=0, hour='*'),  # Runs every 5 minutes
    },
}

# celery timezone
c_app.conf.timezone = "UTC"
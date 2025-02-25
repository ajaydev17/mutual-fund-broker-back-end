from src.mail import mail, create_message
from asgiref.sync import async_to_sync
from typing import List
from src.celery import c_app
import requests
from src.config import config_obj
from celery.exceptions import Retry

# API URL for NAV updates
API_URL = f"http://{config_obj.DOMAIN}/api/v1/investments/update-all-navs"

@c_app.task()
def send_email(recipients: List[str], subject: str, body: str):
    # Celery task to send emails
    message = create_message(recipients=recipients, subject=subject, body=body)
    async_to_sync(mail.send_message)(message)
    print("Email sent successfully!")

@c_app.task(name="src.celery_tasks.check_investments", autoretry_for=(requests.RequestException,), retry_kwargs={"max_retries": 3, "countdown": 60})
def check_investments():
    # Celery task to check investments every 5 minutes.

    try:
        response = requests.post(API_URL, timeout=15)
        response.raise_for_status()
        data = response.json()
        print(f"NAV update API response: {data}")
        return data
    except requests.RequestException as e:
        print(f"Error calling NAV update API: {e}")
        raise Retry(exc=e)
    except Exception as e:
        print(f"Unexpected error: {e}")
        raise e
from fastapi_mail import FastMail, ConnectionConfig, MessageSchema, MessageType
from src.config import config_obj
from pathlib import Path
from typing import List

BASE_DIR = Path(__file__).resolve().parent

# create mail configuration
mail_config = ConnectionConfig(
    MAIL_USERNAME=config_obj.MAIL_USERNAME,
    MAIL_PASSWORD=config_obj.MAIL_PASSWORD,
    MAIL_FROM=config_obj.MAIL_FROM,
    MAIL_PORT=587,
    MAIL_SERVER=config_obj.MAIL_SERVER,
    MAIL_FROM_NAME=config_obj.MAIL_FROM_NAME,
    MAIL_STARTTLS=True,
    MAIL_SSL_TLS=False,
    USE_CREDENTIALS=True,
    VALIDATE_CERTS=True,
)

# create mail object
mail = FastMail(config=mail_config)

# create message schema
def create_message(recipients: List[str], subject: str, body: str):
    # create the message

    message = MessageSchema(
        recipients=recipients,
        subject=subject,
        body=body,
        subtype=MessageType.html
    )

    return message
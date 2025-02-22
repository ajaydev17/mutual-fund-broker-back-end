from passlib.context import CryptContext
from datetime import datetime, timedelta
from src.config import config_obj
import jwt
import uuid
import logging

# create the password context
password_context = CryptContext(
    schemes=['bcrypt']
)

# generate password hash from password
def generate_password_hash(password: str) -> str:
    password_hash = password_context.hash(password)
    return password_hash

# verify password hash from password
def verify_password_hash(password: str, password_hash: str) -> bool:
    return password_context.verify(password, password_hash)
from passlib.context import CryptContext
from datetime import datetime, timedelta
from src.config import config_obj
import jwt
import uuid
import logging
from itsdangerous import URLSafeTimedSerializer

# access token expiry time
ACCESS_TOKEN_EXPIRY = 3600

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

# create jwt access token on successful login
def create_access_token(user_data: dict, expiry: timedelta = None, refresh: bool = False):
    # create the payload
    payload = {
        'user': user_data,
        'exp': datetime.now() + (expiry if expiry else timedelta(seconds=ACCESS_TOKEN_EXPIRY)),
        'jti': str(uuid.uuid4()),
        'refresh': refresh
    }

    # create the token using payload
    token = jwt.encode(
        payload=payload,
        key=config_obj.JWT_SECRET_KEY,
        algorithm=config_obj.JWT_ALGORITHM
    )

    return token

# method which will decode the jwt token
def decode_access_token(token: str) -> dict:
    try:
        token_data = jwt.decode(
            jwt=token,
            key=config_obj.JWT_SECRET_KEY,
            algorithms=[config_obj.JWT_ALGORITHM]
        )

        return token_data
    except jwt.PyJWTError as e:
        logging.exception(e)
        return None

# create a serializer for url safer
serializer = URLSafeTimedSerializer(
    secret_key=config_obj.JWT_SECRET_KEY, salt="email-configuration"
)

# create an url safe token
def create_url_safe_token(data: dict):
    token = serializer.dumps(data)
    return token

# decode the url token
def decode_url_safe_token(token: str):
    try:
        token_data = serializer.loads(token)
        return token_data
    except Exception as e:
        logging.error(str(e))
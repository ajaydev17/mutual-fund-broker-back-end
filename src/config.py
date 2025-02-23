from pydantic_settings import BaseSettings, SettingsConfigDict


# we will load the env variables from this class
class Settings(BaseSettings):
    DATABASE_URL: str
    JWT_SECRET_KEY: str
    JWT_ALGORITHM: str
    REDIS_URL: str = 'redis://localhost:6379/0'
    MAIL_USERNAME: str
    MAIL_PASSWORD: str
    MAIL_FROM: str
    MAIL_PORT: int
    MAIL_SERVER: str
    MAIL_FROM_NAME: str
    MAIL_STARTTLS: bool = True
    MAIL_SSL_TLS: bool = False
    USE_CREDENTIALS: bool = True
    VALIDATE_CERTS: bool = True
    DOMAIN: str
    RAPID_API_URL: str
    RAPID_API_KEY: str
    RAPID_API_HOST: str

    # config the model what to get from the env file
    model_config = SettingsConfigDict(
        env_file='.env',
        extra='ignore'
    )

# create an instance of the settings object
config_obj = Settings()

# celery configuration
broker_url = config_obj.REDIS_URL
result_backend = config_obj.REDIS_URL
broker_connection_retry_on_startup = True

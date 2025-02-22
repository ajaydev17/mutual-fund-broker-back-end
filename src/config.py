from pydantic_settings import BaseSettings, SettingsConfigDict


# we will load the env variables from this class
class Settings(BaseSettings):
    DATABASE_URL: str

    # config the model what to get from the env file
    model_config = SettingsConfigDict(
        env_file='.env',
        extra='ignore'
    )

# create an instance of the settings object
config_obj = Settings()
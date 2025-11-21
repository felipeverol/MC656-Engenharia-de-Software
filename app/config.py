from pydantic import SecretStr 
from pydantic_settings import BaseSettings, SettingsConfigDict

class Settings(BaseSettings):
    MAIL_USERNAME: str
    MAIL_PASSWORD: SecretStr 
    MAIL_FROM: str
    MAIL_PORT: int
    MAIL_SERVER: str

    model_config = SettingsConfigDict(env_file=".env", extra="ignore")

settings = Settings() # type: ignore
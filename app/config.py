from pydantic_settings import BaseSettings, SettingsConfigDict

class Settings(BaseSettings):
    # Define as variáveis esperadas. O Pydantic vai buscar nomes iguais no .env
    MAIL_USERNAME: str
    MAIL_PASSWORD: str
    MAIL_FROM: str
    MAIL_PORT: int
    MAIL_SERVER: str

    # Configuração para ler do arquivo .env
    model_config = SettingsConfigDict(env_file=".env", extra="ignore")

# Instancia as configurações para usar no resto do app
settings = Settings()
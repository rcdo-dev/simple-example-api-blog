from pydantic_settings import BaseSettings, SettingsConfigDict


# Definição da classe de configurações.
class Settings(BaseSettings):
    # JWT Settings (Valores padrão).
    SECRET_KEY: str = "sua_chave_secreta_padrao_para_desenvolvimento_troque_em_prod"
    ALGOTITHM: str = "HS256"
    ACCESS_TOKEN_EXPIRE_MINUTES: int = 30

    # Database Settings
    DATABASE_URL: str = "sqlite:/// ./blog.db"

    # Configuração do Pydantic para carregar de um arquivo .env.
    # O Pydantic irá primeiro procurar variáveis de ambiente e, em seguida,
    # tentar ler o arquivo .env se ele existir.
    model_config = SettingsConfigDict(env_file=".env", extra="ignore")


# Instância única da configuração.
settings = Settings()

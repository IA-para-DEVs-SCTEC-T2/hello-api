import os
from dotenv import load_dotenv

load_dotenv()


class Settings:
    """Centraliza todas as configurações da aplicação via variáveis de ambiente."""

    secret_key: str = os.getenv("SECRET_KEY", "")
    algorithm: str = os.getenv("ALGORITHM", "HS256")
    access_token_expire_minutes: int = int(os.getenv("ACCESS_TOKEN_EXPIRE_MINUTES", "30"))
    professor_username: str = os.getenv("PROFESSOR_USERNAME", "")
    professor_password: str = os.getenv("PROFESSOR_PASSWORD", "")


settings = Settings()

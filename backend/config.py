from pydantic import field_validator
from pydantic_settings import BaseSettings

# A stable hardcoded dev secret — never empty, never changes between restarts.
# Override via JWT_SECRET_KEY in .env for production.
_HARDCODED_DEV_SECRET = "aikos-dev-2024-xK9mP2nL8qR5vT7yW3jF6hD1cB4eA0"


class Settings(BaseSettings):
    gemini_api_key: str = ""
    jwt_secret_key: str = _HARDCODED_DEV_SECRET
    jwt_algorithm: str = "HS256"
    jwt_expire_minutes: int = 1440
    chroma_persist_dir: str = "./chroma_db"

    @field_validator("jwt_secret_key")
    @classmethod
    def jwt_secret_not_empty(cls, v: str) -> str:
        """If the env var is blank, use the hardcoded dev secret."""
        stripped = v.strip()
        return stripped if stripped else _HARDCODED_DEV_SECRET

    class Config:
        env_file = ".env"


settings = Settings()

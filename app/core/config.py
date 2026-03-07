from datetime import timedelta
from pathlib import Path

from pydantic import SecretStr
from pydantic_settings import BaseSettings, SettingsConfigDict

ROOT_DIR = Path(__file__).resolve().parent.parent.parent
APP_DIR = ROOT_DIR / "app"

DATABASE_URL = f"sqlite+aiosqlite:///{APP_DIR / 'blog.db'}"


class Settings(BaseSettings):
    model_config = SettingsConfigDict(
        env_file=ROOT_DIR / ".env",
        env_file_encoding="utf-8",
    )

    jwt_secret_key: SecretStr
    algorithm: str = "HS256"
    access_token_expire_minutes: int = 30

    @property
    def access_token_expire_delta(self) -> timedelta:
        return timedelta(minutes=self.access_token_expire_minutes)


settings = Settings()  # type: ignore [call-arg] # Cargado desde archivo .env

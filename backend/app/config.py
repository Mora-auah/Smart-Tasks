from functools import lru_cache
from pathlib import Path

from pydantic_settings import BaseSettings, SettingsConfigDict

ROOT = Path(__file__).resolve().parents[2]


class Settings(BaseSettings):
    model_config = SettingsConfigDict(env_file=ROOT.parent / ".env", extra="ignore")

    openai_api_key: str = ""
    model_daily_summary: str = ""
    model_chat: str = ""
    host: str = "127.0.0.1"
    port: int = 8000
    timezone: str = "Asia/Jerusalem"
    database_url: str = f"sqlite:///{ROOT / 'data' / 'smart_tasks.db'}"


@lru_cache
def get_settings() -> Settings:
    return Settings()

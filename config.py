from functools import lru_cache

from pydantic import field_validator
from pydantic_settings import BaseSettings, SettingsConfigDict


class Settings(BaseSettings):
    model_config = SettingsConfigDict(env_file=".env", env_file_encoding="utf-8")

    # Proxy target
    target_api_url: str = "https://api.openai.com"
    target_api_key: str = ""

    # Vault
    vault_db_path: str = ""  # empty = in-memory SQLite
    vault_ttl_seconds: int = 3600

    # Locale plugins
    locales: list[str] = []

    # Universal detectors
    detect_email: bool = True
    detect_iban: bool = True
    detect_credit_card: bool = True
    detect_phone: bool = True
    detect_ip: bool = True
    detect_url_credentials: bool = True
    detect_names: bool = True

    @field_validator("locales", mode="before")
    @classmethod
    def parse_locales(cls, v: object) -> list[str]:
        if isinstance(v, str):
            return [loc.strip().lower() for loc in v.split(",") if loc.strip()]
        return v  # type: ignore[return-value]


@lru_cache
def get_settings() -> Settings:
    return Settings()

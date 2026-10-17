from __future__ import annotations

from pydantic_settings import BaseSettings, SettingsConfigDict
from pydantic import Field, model_validator


class Settings(BaseSettings):
    database_url: str | None = Field(default=None, validation_alias="db_url")
    # another config or environmental variables...

    model_config = SettingsConfigDict(
        env_file=".env",
        env_file_encoding="utf-8",
        extra="ignore",
    )

    @model_validator(mode="after")
    def validate_database_url(self) -> Settings:
        if not self.database_url:
            raise ValueError("環境變數中缺少必要的 'db_url' 或 'database_url' 設定")
        return self


settings = Settings()

__all__ = ["settings"]
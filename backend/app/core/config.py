from __future__ import annotations

from pydantic_settings import BaseSettings, SettingsConfigDict
from pydantic import Field, model_validator, computed_field


class Settings(BaseSettings):
    raw_database_url: str | None = Field(default=None, validation_alias="db_url", repr=False)
    # another config or environmental variables...

    model_config = SettingsConfigDict(
        env_file=".env",
        env_file_encoding="utf-8",
        extra="ignore",
    )

    @model_validator(mode="after")
    def validate_database_url(self) -> Settings:
        if not self.raw_database_url:
            raise ValueError("環境變數中缺少必要的 'db_url' 或 'database_url' 設定")
        return self

    @computed_field
    @property
    def database_url(self) -> str:
        assert self.raw_database_url is not None
        return self.raw_database_url


settings = Settings()

__all__ = ["settings"]
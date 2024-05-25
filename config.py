import os
from functools import lru_cache
from os import path
from typing import Any, Dict
from pydantic_settings import BaseSettings


AnyDict = Dict[str, Any]
BASE_DIR: str = path.abspath(path.dirname(path.dirname(__file__)))


class Settings(BaseSettings):
    class Config:
        env_file: str = os.path.join(os.path.dirname(__file__), ".env")
        env_file_encoding: str = "utf-8"
        case_sensitive: bool = True
        extra = "allow"

    debug: bool = False
    docs_url: str = "/docs"
    openapi_url: str = "/openapi.json"
    redoc_url: str = "/redoc"
    title: str = "Travel Recommenation"
    version: str = "0.1.0"

    LOG_LEVEL: str = "INFO"
    OPENAI_API_KEY: str

    @property
    def fastapi_kwargs(self) -> dict[str, Any]:
        return {
            "debug": self.debug,
            "docs_url": self.docs_url,
            "openapi_url": self.openapi_url,
            "redoc_url": self.redoc_url,
            "title": self.title,
            "version": self.version,
        }


@lru_cache
def get_settings():
    return Settings()  # type: ignore


settings = get_settings()

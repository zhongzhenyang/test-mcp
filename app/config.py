from __future__ import annotations

import os
from dataclasses import dataclass
from dotenv import load_dotenv

load_dotenv()


@dataclass(frozen=True)
class Settings:
    app_name: str
    app_env: str
    log_level: str
    service_a_base_url: str
    service_a_username: str
    service_a_password: str
    http_timeout: float


def load_settings() -> Settings:
    return Settings(
        app_name=os.getenv("APP_NAME", "service-b-mcp"),
        app_env=os.getenv("APP_ENV", "dev"),
        log_level=os.getenv("LOG_LEVEL", "INFO"),
        service_a_base_url=os.getenv("SERVICE_A_BASE_URL", "http://localhost:8080").rstrip("/"),
        service_a_username=os.getenv("SERVICE_A_USERNAME", "admin"),
        service_a_password=os.getenv("SERVICE_A_PASSWORD", "123456"),
        http_timeout=float(os.getenv("HTTP_TIMEOUT", "30")),
    )

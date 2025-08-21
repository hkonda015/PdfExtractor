from __future__ import annotations

import os

from dotenv import load_dotenv
from pydantic import BaseModel

load_dotenv()


class Settings(BaseModel):
    base_url: str | None = os.getenv("BASE_URL")
    api_key: str | None = os.getenv("API_KEY")
    timeout: int = int(os.getenv("TIMEOUT", "30"))
    log_level: str = os.getenv("LOG_LEVEL", "INFO")


settings = Settings()

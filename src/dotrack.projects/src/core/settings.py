import logging
import os
from pathlib import Path

from pydantic_settings import BaseSettings, SettingsConfigDict

env_file = Path(__file__).parent.parent.parent / f"{os.environ.get('APP_CONFIG_FILE', '')}.env"

logger = logging.getLogger(__name__)


class Settings(BaseSettings):
    DEBUG: bool | None = False
    API_V1_STR: str = "/api/v1"

    DB_URI: str
    ECHO_SQL: bool = True

    SECRET_KEY: str = "secret"
    ALGORITHM: str = "HS256"
    ACCESS_TOKEN_EXPIRE_MINUTES: int = 60 * 24 * 7

    model_config = SettingsConfigDict(
        env_file=env_file,
        case_sensitive=True,
    )


if not Path(env_file).exists():
    raise Exception(f"Configuration file not found. {env_file}")


settings = Settings.model_validate({})

# TODO: Add logging
logger.debug(f"Configuration file: {env_file}")
logger.debug(f"Settings: {settings}")

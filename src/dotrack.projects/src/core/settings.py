import os
from pathlib import Path

from pydantic_settings import BaseSettings, SettingsConfigDict

env_file = Path(__file__).parent.parent.parent / f"{os.environ.get('APP_CONFIG_FILE', '')}.env"


class Settings(BaseSettings):
    DB_URI: str
    ECHO_SQL: bool = True

    model_config = SettingsConfigDict(
        env_file=env_file,
        case_sensitive=True,
    )


if not Path(env_file).exists():
    raise Exception(f"Configuration file not found. {env_file}")

print(Path(__file__).parent / f"config/{os.environ.get('APP_CONFIG_FILE', '')}.env")
settings = Settings.model_validate({})

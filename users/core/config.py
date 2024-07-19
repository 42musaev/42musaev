from pathlib import Path

from pydantic_settings import BaseSettings
from pydantic_settings import SettingsConfigDict

BASEDIR = Path(__file__).parent.parent
ENV_FILE = BASEDIR / 'env' / '.env.users'


class Settings(BaseSettings):
    model_config = SettingsConfigDict(env_file=ENV_FILE, extra='ignore')

    domain: str = 'localhost'
    echo_sql: bool = True
    DATABASE_URL: str


settings = Settings()

from pathlib import Path

from pydantic_settings import BaseSettings
from pydantic_settings import SettingsConfigDict

BASEDIR = Path(__file__).parent.parent
ENV_FILE = BASEDIR / 'env' / '.env.auth'


class JWTSettings(BaseSettings):
    private_key: Path = BASEDIR / 'certs' / 'jwt-private.pem'
    public_key: Path = BASEDIR / 'certs' / 'jwt-public.pem'
    algorithm: str = 'RS256'
    access_token_expire_minutes: int = 30
    refresh_token_expire_days: int = 90


class Settings(BaseSettings):
    model_config = SettingsConfigDict(env_file=ENV_FILE, extra='ignore')
    jwt_settings: JWTSettings = JWTSettings()

    domain: str = 'localhost'

    echo_sql: bool = True
    DATABASE_URL: str


settings = Settings()

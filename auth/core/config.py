from pathlib import Path

from pydantic_settings import BaseSettings

BASEDIR = Path(__file__).parent.parent


class JWTSettings(BaseSettings):
    private_key: Path = BASEDIR / 'certs' / 'jwt-private.pem'
    public_key: Path = BASEDIR / 'certs' / 'jwt-public.pem'
    algorithm: str = 'RS256'
    access_token_expire_minutes: int = 3


class Settings(BaseSettings):
    jwt_settings: JWTSettings = JWTSettings()
    database_url: str = 'asyncpg://postgres:password@db:5432/mydatabase'
    echo_sql: bool = True


settings = Settings()

import os
from dataclasses import dataclass

from pydantic import SecretStr

@dataclass(frozen=True)
class Settings:
    database_url: str = "postgresql+asyncpg://auth:auth@auth-db:5432/auth"
    jwt_secret: SecretStr = SecretStr("ubciqurewytf91785qiugyrbq98761hj09r8etnjlgbeyufgbsl")
    jwt_algorithm: str = "HS256"
    jwt_access_token_expire_minutes: int = 30


settings = Settings()
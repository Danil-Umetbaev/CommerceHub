from pydantic import SecretStr, Field
from pydantic_settings import BaseSettings


class Settings(BaseSettings):
    database_url: str = "postgresql+asyncpg://auth:auth@auth-db:5432/auth"
    jwt_secret: SecretStr = SecretStr("ubciqurewytf91785qiugyrbq98761hj09r8etnjlgbeyufgbsld")
    jwt_algorithm: str = "HS256"
    cors_origin: list[str] = Field(["*"])
    CATALOG_SERVICE_URL: str = "http://catalog-service:8000"
    ORDER_SERVICE_URL: str = "http://order-service:8000"
    AUTH_SERVICE_URL: str = "http://auth-service:8000"


settings = Settings()
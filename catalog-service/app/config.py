import os
from dataclasses import dataclass

@dataclass(frozen=True)
class Settings:
    database_url: str

def get_settings() -> Settings:
    return Settings(
        database_url=os.getenv(
            "DATABASE_URL",
            "postgresql+psycopg2://catalog:catalog@catalog-db:5432/catalog"
        )
    )
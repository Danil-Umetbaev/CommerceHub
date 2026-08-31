from pydantic_settings import BaseSettings, SettingsConfigDict

class Settings(BaseSettings):

    kafka_bootstrap_servers: str = 'localhost:9092'
    kafka_topic: str = 'payments-events'
    mongodb_url: str = 'mongodb://analytics:analytics@localhost:27017/analytics'
    mongodb_database: str = 'analytics'
    mongodb_collection: str = 'events'


settings = Settings()

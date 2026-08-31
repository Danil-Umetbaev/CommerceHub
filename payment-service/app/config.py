import os
from dataclasses import dataclass

@dataclass(frozen=True)
class Settings:
    database_url: str
    base_url_catalog_client: str
    rabbitmq_url: str
    payment_succeeded_routing_key: str
    payment_exchange_name: str
    kafka_bootstrap_server: str
    kafka_analytic_payment_topic: str

def get_settings() -> Settings:
    return Settings(
        database_url=os.getenv(
            "DATABASE_URL",
            "postgresql+asyncpg://postgres:postgres@127.0.0.1:5432/payment_microservices"
        ),
        base_url_catalog_client=os.getenv(
            "BASE_URL_CATALOG_CLIENT",
            "http://127.0.0.1:8002/payments"
        ),
        rabbitmq_url=os.getenv("RABBITMQ_URL", "amqp://guest:guest@localhost:5672"),
        payment_succeeded_routing_key=os.getenv("PAYMENT_SUCCEEDED_ROUTING_KEY", "payment.succeeded"),
        payment_exchange_name=os.getenv("PAYMENT_EXCHANGE_NAME", "payment.events"),
        kafka_bootstrap_server='kafka:29092',
        kafka_analytic_payment_topic='payments-events'
    )